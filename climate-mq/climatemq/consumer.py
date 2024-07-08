import json
import pika
import threading
from django.contrib.gis.geos import Point

from climatemq.models import Station, Unit, Variable, Data

ROUTING_KEY = 'sensor.temperature'
EXCHANGE = 'user_exchange'
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
        self.channel.basic_qos(prefetch_count=THREADS*10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        
    def callback(self, channel, method, properties, body):
        print(f"arrived {body}")
        self.saveData(body)
        print(f" [x] {method.routing_key} saved:{body}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        
    def run(self):
        print ('Created Consumer ')
        self.channel.start_consuming()

    def saveData(self, body):
        json_response = json.loads(body)
        
        print(json_response)
        print(json_response['location']['longitude'])

        pnt = Point(json_response['location']['longitude'], json_response['location']['latitude'])
    

        station = Station.objects.get(location=pnt)
        station.consuming = True
        station.save()

        print(json_response['unit'])

        unit = Unit.objects.get(symbol=json_response['unit'])
        variable = Variable.objects.get(unit=unit)

        new_data = Data(station=station, variable=variable, value=json_response['detectedData'])
        Data.save(new_data)
        station.consuming = False
        station.save()
