import json
import pika
import threading
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from climatemq.models import Station, Unit, Variable, Data, Goal

ROUTING_KEY = 'sensor.detected'
ROUTING_KEY_NEW = 'station.new'
EXCHANGE = 'data'
THREADS = 5

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange='data', exchange_type='topic', durable=True)

        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange='data', queue=queue_name, routing_key=ROUTING_KEY)
        self.channel.queue_bind(exchange='data', queue=queue_name, routing_key=ROUTING_KEY_NEW)
        self.channel.basic_qos(prefetch_count=THREADS*10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        
    def callback(self, channel, method, properties, body):
        try:
            print(f"arrived {body}")
            if (method.routing_key == ROUTING_KEY_NEW):
                self.newStation(body)
            elif (method.routing_key == ROUTING_KEY):
                self.saveData(body)
                print(f" [x] {method.routing_key} saved:{body}")
        except Exception as e:
            print(f"Error processing message: {e}")
        
        channel.basic_ack(delivery_tag=method.delivery_tag)
        
    def run(self):
        print ('Created Consumer ')
        self.channel.start_consuming()

    def newStation(self, body):
        json_response = json.loads(body)['station']

        if not User.objects.filter(username=json_response['username']).exists():
            user = User.objects.create_user(json_response['username'],password=json_response['key'])
            user.save()

        pnt = Point(json_response['location']['longitude'], json_response['location']['latitude'])

        if not Station.objects.filter(location=pnt).exists():
            new_station = Station.objects.create(name=json_response['name'], location=pnt)
            new_station.save()

    def saveData(self, body):
        json_response = json.loads(body)

        print(json_response)
        print(json_response['station']['location']['longitude'])

        pnt = Point(
            json_response['station']['location']['longitude'],
            json_response['station']['location']['latitude']
        )

        try:
            station = Station.objects.get(location=pnt)
            if not station.status == "ACTIVE":
                Station.objects.filter(id=station.id).update(status='ACTIVE')
        except Station.DoesNotExist:
            print(f"Station at {pnt} not found.")
            return

        if station.accepted:
            user = authenticate(
                username=json_response['station']['username'],
                password=json_response['station']['key']
            )
            if user is not None:
                unit = Unit.objects.get(symbol=json_response['unit'])
                variable = Variable.objects.get(unit=unit)
                current_value = json_response['detectedData']
                battery_level = json_response.get('battery', 100.0)

                Data.objects.create(
                    station=station,
                    variable=variable,
                    value=current_value,
                    created_at=timezone.now()
                )

                Station.objects.filter(id=station.id).update(battery_level=battery_level)

                # --- COLLECT COMMANDS FROM BOTH STRATEGIES -------
                goal_commands = self.apply_goal_strategy(station, variable, current_value)
                battery_commands = self.apply_battery_strategy(station, battery_level)

                # Merge commands: if a station appears in both lists,
                # multiply the rates (if both are SCALE_RATE) and keep the battery command.
                merged = {}
                for sname, action, value in battery_commands:
                    merged[sname] = (action, value)

                for sname, action, value in goal_commands:
                    if sname in merged:
                        b_action, b_value = merged[sname]
                        # Only multiply if both are SCALE_RATE
                        if action == 'SCALE_RATE' and b_action == 'SCALE_RATE':
                            merged[sname] = (b_action, b_value * value)
                        # If goal command is not a rate, keep the battery command
                        # (no change needed)
                    else:
                        merged[sname] = (action, value)

                # Send every command once
                for sname, (act, val) in merged.items():
                    self.send_command(sname, act, val)

    # --- STRATEGY A: BATTERY LOGIC ---
    def apply_battery_strategy(self, station, battery):
        """
        Manages Lifecycle based on energy.
        Uses SCALING factors (Percentage) rather than absolute rates.
        1.0 = 100% (Normal), 0.5 = 50% (Slow), 2.0 = 200% (Fast)
        """
        commands = []
        neighbor = self.get_nearest_neighbor(station)

        if battery < 20.0:
            # CRITICAL: shut down self, scale neighbor
            commands.append((station.name, 'SWITCH', 'OFF'))
            Station.objects.filter(id=station.id).update(status='INACTIVE')
            if neighbor:
                commands.append((neighbor.name, 'SCALE_RATE', 2.0))

        elif battery < 40.0:
            # LOW: throttle self, help neighbor
            commands.append((station.name, 'SCALE_RATE', 0.5))
            if neighbor:
                commands.append((neighbor.name, 'SCALE_RATE', 1.5))

        return commands

    # --------------------------------------------------------------------
    # --- STRATEGY B: GOAL LOGIC -----------------------------------------
    # --------------------------------------------------------------------
    def apply_goal_strategy(self, station, variable, value):
        """
        Checks User-defined thresholds (Goals).
        If violated, alerts neighborhood.
        """
        commands = []
        goals = Goal.objects.filter(variable=variable, is_active=True)

        for goal in goals:
            violated = False
            if goal.operator == '>' and value > goal.threshold:
                violated = True
            elif goal.operator == '<' and value < goal.threshold:
                violated = True
            elif goal.operator == '==' and value == goal.threshold:
                violated = True

            if violated:
                print(f" [Plan] GOAL VIOLATED: {goal.name}. Alerting Neighborhood.")
                nearby = Station.objects.filter(
                    location__distance_lte=(station.location, D(km=5))
                )

                for s in nearby:
                    if goal.action:
                        commands.append((s.name, 'ACTION', goal.action.command_key))

        return commands

    # --- ACTUATOR ---
    def send_command(self, station_name, action, value):
        """
        Publishes command to RabbitMQ.
        """
        payload = json.dumps({"action": action, "value": value})
        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=f'station.control.{station_name}',
            body=payload
        )
        print(f" [Execute] Sent {action}={value} to Station_{station_name}")

    # --- GIS HELPER ---
    def get_nearest_neighbor(self, station):
        """Finds the closest station to transfer load to."""
        return Station.objects.exclude(id=station.id).exclude(status="INACTIVE") \
                    .annotate(distance=Distance('location', station.location)) \
                    .annotate(battery_distance=F('battery_level') - F('distance')) \
                    .order_by('-battery_distance') \
                    .first()

    # def is_goal_violated(self, goal, value):
    #     """Simple Planning logic to check thresholds"""
    #     if goal.operator == '>': return value > goal.threshold
    #     if goal.operator == '<': return value < goal.threshold
    #     if goal.operator == '==': return value == goal.threshold
    #     return False
    
    # def execute_actuator_command(self, station_id, action, value):
    #     """
    #     Acts as the 'Actuator' by sending a control message back to the station.
    #     """
    #     # Define the payload for the physical station to interpret
    #     message = {
    #         "action": action, # 'SET_RATE' or 'SWITCH'
    #         "value": value    # e.g., 1.0 or 'OFF'
    #     }
        
    #     self.channel.basic_publish(
    #         exchange='data',
    #         routing_key=f'station.control.{station_id}',
    #         body=json.dumps(message)
    #     )
    #     self.connection.close()
        
    #     print(f" [x] Sent {message} to Station {station_id}")

    # def handle_strategy(self, station, battery_level):
    #     """
    #     Implements the MAPE-K Strategy:
    #     - 30% threshold: Conservation Mode
    #     - 20% threshold: Critical Recharge Mode
    #     """
        
    #     # 1. ANALYZE: Check Battery Thresholds
    #     if battery_level < 20:
    #         print(f"[PLAN] {station.name} Critical Battery ({battery_level}%). Initiating SHUTDOWN.")
            
    #         # A. Execute on Self: Shut Down
    #         self.send_command(station.id, 'SWITCH', 'OFF')
            
    #         # B. Execute on Neighbor: Max Performance
    #         neighbor = self.get_nearest_neighbor(station)
    #         if neighbor:
    #             print(f"[PLAN] Compensating with neighbor {neighbor.name} (Rate: 1.0s)")
    #             self.send_command(neighbor.id, 'SET_RATE', 1.0)

    #     elif battery_level < 30:
    #         print(f"[PLAN] {station.name} Low Battery ({battery_level}%). Conserving energy.")
            
    #         # A. Execute on Self: Slow Down (e.g., send every 15s)
    #         self.send_command(station.id, 'SET_RATE', 15.0)
            
    #         # B. Execute on Neighbor: Increase Performance (e.g., send every 2s)
    #         neighbor = self.get_nearest_neighbor(station)
    #         if neighbor:
    #             print(f"[PLAN] Boosting neighbor {neighbor.name} (Rate: 2.0s)")
    #             self.send_command(neighbor.id, 'SET_RATE', 2.0)

    # def get_nearest_neighbor(self, station):
    #     """GIS Helper to find the closest OTHER station"""
    #     # Exclude self, order by distance
    #     return Station.objects.exclude(id=station.id)\
    #                         .annotate(distance=Distance('location', station.location))\
    #                         .order_by('distance')\
    #                         .first()

    # def send_command(self, station_id, action, value):
    #     """Actuator Helper"""
    #     payload = json.dumps({"action": action, "value": value})
    #     self.channel.basic_publish(
    #         exchange='user_exchange', 
    #         routing_key=f'station.control.{station_id}', 
    #         body=payload
    #     )

    # def analyze_and_plan(self, station, variable, latest_value):
    #     # Find goals for this variable
    #     goals = Goal.objects.filter(variable=variable, is_active=True)
        
    #     for goal in goals:
    #         # Simple threshold check
    #         if (goal.operator == '>' and latest_value > goal.threshold) or \
    #         (goal.operator == '<' and latest_value < goal.threshold):
                
    #             # GIS Rule: Apply this to all stations within 5km (Spatial Standard)
    #             nearby_stations = Station.objects.filter(
    #                 location__distance_lte=(station.location, D(km=5))
    #             )
                
    #             for s in nearby_stations:
    #                 self.execute_action(s, goal.action)
