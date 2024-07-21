import json
import pika
import threading
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from climatemq.models import Station, Unit, Variable, Data

ROUTING_KEY = 'sensor.detected'
ROUTING_KEY_NEW = 'station.new'
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
        self.channel.queue_bind(exchange='data', queue=queue_name, routing_key=ROUTING_KEY_NEW)
        self.channel.basic_qos(prefetch_count=THREADS*10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        
    def callback(self, channel, method, properties, body):
        print(f"arrived {body}")
        if (method.routing_key == "station.new"):
            self.newStation(body)
        else:
            self.saveData(body)
        print(f" [x] {method.routing_key} saved:{body}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        
    def run(self):
        print ('Created Consumer ')
        self.channel.start_consuming()

    def newStation(self, body):
        json_response = json.loads(body)

        user = User.objects.create_user(json_response['username'],password=json_response['key'])
        user.save()

        pnt = Point(json_response['location']['longitude'], json_response['location']['latitude'])

        new_station = Station.objects.create(name=json_response['name'], location=pnt)
        new_station.save()

    def saveData(self, body):
        json_response = json.loads(body)
        
        print(json_response)
        print(json_response['station']['location']['longitude'])

        pnt = Point(json_response['station']['location']['longitude'], json_response['station']['location']['latitude'])
    

        station = Station.objects.get(location=pnt)
        if (station.accepted == True):
            user = authenticate(username=json_response['station']['username'], password=json_response['station']['key'])
            if user is not None:
                print(json_response['unit'])

                unit = Unit.objects.get(symbol=json_response['unit'])
                variable = Variable.objects.get(unit=unit)

                new_data = Data(station=station, variable=variable, value=json_response['detectedData'], created_at=timezone.now())
                Data.save(new_data) 

