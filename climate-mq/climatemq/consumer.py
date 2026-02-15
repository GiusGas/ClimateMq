import json
import threading
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from climatemq.models import *
from climatemq.utils.rabbit_utils import RabbitManager
from climatemq.analyzer import apply_battery_strategy, apply_goal_strategy, get_nearest_neighbor

ROUTING_KEY = 'sensor.detected'
ROUTING_KEY_NEW = 'station.new'
EXCHANGE = 'data'
THREADS = 5

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.rabbit_manager = RabbitManager()
        self.connection = self.rabbit_manager.get_connection()
        self.channel = self.connection.channel()

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
                battery_level = json_response.get('battery', 100.0)
                sensor_name = station.name+"_"+variable.name
                sensor = Sensor.objects.filter(name=sensor_name).first()
                
                if sensor is None:
                    sensor = Sensor.objects.create(
                        name=sensor_name,
                        station=station,
                        variable=variable,
                        battery_level=battery_level,
                        status='ACTIVE')
                else:
                    sensor.status = 'ACTIVE'
                    sensor.battery_level = battery_level
                    sensor.save()

                current_value = json_response['detectedData']

                if self.validate_and_save_data(sensor=sensor, new_value=current_value):

                    goal_commands = apply_goal_strategy(station, variable, current_value)
                    battery_commands = apply_battery_strategy(station, variable, battery_level)

                    # Merge commands: if a station appears in both lists, multiply the rates
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
                        else:
                            merged[sname] = (action, value)

                    for sname, (act, val) in merged.items():
                        self.rabbit_manager.send_command(sname, act, val, variable.name)

    def validate_and_save_data(self, sensor, new_value):
        goal, _ = SensorGoal.objects.get_or_create(sensor=sensor)

        if sensor.predicted_value is not None:
            variance = abs(new_value - sensor.predicted_value)
            
            if variance > goal.max_variance:
                goal.consecutive_anomalies += 1
                
                if goal.consecutive_anomalies >= 3:
                    goal.is_broken = True
                    sensor.status = "BROKEN"
                    sensor.save()
                    goal.save()
                    print(f"STRIKE 3: Shutting down broken sensor {sensor.id}")
                    self.rabbit_manager.send_command(sensor.station.name, "SWITCH", "OFF", sensor.variable.name)
                    nearest = get_nearest_neighbor(sensor.station, sensor.variable)
                    self.rabbit_manager.send_command(nearest.name, "SCALE_RATE", 2.0, sensor.variable.name)
                    return False
                
                else:
                    goal.save()
                    self.rabbit_manager.send_command(sensor.station.name, "SCALE_RATE", 5.0, sensor.variable.name)
                    print(f"STRIKE {goal.consecutive_anomalies}: Increasing rate for {sensor.id}")
                    return False

        if goal.consecutive_anomalies > 0:
            goal.consecutive_anomalies = 0
            goal.save()

        Data.objects.create(
            sensor=sensor,
            variable=sensor.variable,
            value=new_value
        )
        return True
