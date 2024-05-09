from django.shortcuts import render
import pika
import sys

from climatemq.models import Station

from django.views.generic.base import (
    TemplateView,
)

class StationsMapView(TemplateView):
    template_name = "map.html"

def get_long_and_lat(station): 
    long = station.location.coords[0]
    lat = station.location.coords[1]
    return (long,lat)

def read_temperature():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='tut.topic', exchange_type='topic', durable=True)

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    stations = Station.objects.all()
    coordinates = [get_long_and_lat(station) for station in stations]

    binding_keys = ['sensor.temperature.'+str('%.1f'%(long))+'.'+str('%.1f'%(lat)) for (long,lat) in coordinates]

    for binding_key in binding_keys:
        print(binding_key)
        channel.queue_bind(
            exchange='tut.topic', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(f" [x] {method.routing_key}:{body}")


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
