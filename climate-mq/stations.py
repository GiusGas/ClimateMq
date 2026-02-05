import multiprocessing
import time
import json
import random
import pika

DRAIN_RATE = 10.0
RECHARGE_RATE = 0.5

class ManagedStation(multiprocessing.Process):
    def __init__(self, station_id, station_name):
        super(ManagedStation, self).__init__()
        self.station_id = station_id
        self.station_name = f"{station_name}_{station_id}"
        self.reporting_interval = 5.0
        self.is_active = True
        self.battery = 60.0

        self.routing_key_data = 'sensor.detected'
        self.routing_key_control = f'station.control.{self.station_name}'

        self.send_initial_station_message()

    def send_initial_station_message(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        
        # Declare Exchanges
        channel.exchange_declare(exchange='data', exchange_type='topic', durable=True)
        
        payload = {
            "station": {
                "name": self.station_name,
                "location": {"longitude": 12.0 + (self.station_id * 0.1), "latitude": 41.0},
                "username": self.station_name, 
                "key": self.station_name
            }
        }
        
        channel.basic_publish(exchange='data', routing_key='station.new', body=json.dumps(payload))
        connection.close()
        print(f"[*] {self.station_name} sent initial message to station.new")

    def handle_command(self, ch, method, properties, body):
        """THE EFFECTOR: Acts on signals from the MAPE-K Execute phase"""
        command = json.loads(body)
        action = command.get('action')
        value = command.get('value')

        if action == 'SCALE_RATE':
            # Base interval is 5.0 seconds. 
            # If value is 0.5 (slow), interval becomes 10s.
            # If value is 2.0 (fast), interval becomes 2.5s.
            # Formula: New Interval = Base / Scale
            scale = float(value)
            self.reporting_interval = 5.0 / scale 
            print(f"[{self.station_name}] 📶 RATE SCALED x{scale} -> {self.reporting_interval:.1f}s")
        
        elif action == 'SWITCH':
            self.is_active = (value == 'ON')
            status = "RESUMED" if self.is_active else "SHUTDOWN"
            print(f"[{self.station_name}] STATE: {status}")

    def run(self):
        # Connection must be created inside the process
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Declare Exchanges
        channel.exchange_declare(exchange='data', exchange_type='topic', durable=True)
        
        # Setup Control Listener
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='data', queue=queue_name, routing_key=self.routing_key_control)
        channel.basic_consume(queue=queue_name, on_message_callback=self.handle_command, auto_ack=True)

        print(f"[*] {self.station_name} online. Listening on {self.routing_key_control}")

        last_send_time = time.time()
        try:
            while True:
                # Check for incoming control signals (Non-blocking)
                connection.process_data_events(time_limit=0.1)

                # Send data ONLY if active (The Monitor Input)
                if self.is_active and (time.time() - last_send_time > self.reporting_interval):
                    print(f"[{self.station_name}] Sending data...")
                    drain = random.uniform(0.1, DRAIN_RATE*(5.0/self.reporting_interval))
                    self.battery = max(0, self.battery - drain)
                    
                    payload = {
                        "station": {
                            "name": self.station_name,
                            "location": {"longitude": 12.0 + (self.station_id * 0.1), "latitude": 41.0},
                            "username": self.station_name, "key": self.station_name
                        },
                        "unit": "°C",
                        "detectedData": round(random.uniform(20, 30), 2),
                        "battery": round(self.battery, 2)
                    }
                    channel.basic_publish(exchange='data', routing_key=self.routing_key_data, body=json.dumps(payload))
                    last_send_time = time.time()
                else:
                        if not self.is_active and self.battery == 100:
                            self.is_active = True
                            print(f"[{self.station_name}] Battery depleted. Auto-RESUMING operation for recharge.")
                        else:
                            self.battery = min(100, self.battery + RECHARGE_RATE)

                            if int(self.battery) % 10 == 0: 
                                print(f"[{self.station_name}] ...Recharging... {self.battery:.1f}%")
                        
                        time.sleep(1.0)
        except KeyboardInterrupt:
            connection.close()

if __name__ == "__main__":
    import sys
    num_stations = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    
    processes = []
    for i in range(num_stations):
        p = ManagedStation(i, "Rome_Station")
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
