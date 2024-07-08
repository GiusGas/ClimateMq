from django.shortcuts import render
import pika
import sys
import json
from django.contrib.gis.geos import Point

from climatemq.models import Station, Unit, Variable, Data

from django.views.generic.base import (
    TemplateView,
    View
)

class StationsMapView(TemplateView):
    template_name = "map.html"

class StationsListView(View):
    template_name = "station_list.html"

    def get(self, request, *args, **kwargs):
        station_list = get_station_list()
        print(station_list[0].location.coords[1])
        return render(request, self.template_name, {"station_list":station_list})

class StationsDashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        station_list = get_station_list()
        return render(request, self.template_name, {"station_list":station_list})
    
class StationDashboardView(View):
    template_name = "dashboard.html"
    
    def get(self, request, station_id, *args, **kwargs):
        station_list = get_station_list()
        data_list = get_data_list(station_id)
        print(data_list)
        return render(request, self.template_name, {"data_list":data_list, "station_list":station_list})

def get_station_list():
    return Station.objects.all()

def get_data_list(station_id):
    return Data.objects.filter(station_id=station_id)

def get_long_and_lat(station): 
    long = station.location.coords[0]
    lat = station.location.coords[1]
    return (long,lat)

def read_temperature():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='data', exchange_type='topic', durable=True)

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    stations = Station.objects.all()
    coordinates = [get_long_and_lat(station) for station in stations]

    #binding_keys = ['sensor.temperature.'+str('%.1f'%(long))+'.'+str('%.1f'%(lat)) for (long,lat) in coordinates]
    binding_key = 'sensor.temperature'
    #for binding_key in binding_keys:
        #print(binding_key)
    channel.queue_bind(
        exchange='data', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        saveData(body)
        print(f" [x] {method.routing_key} saved:{body}")


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

def saveData(body):
    json_response = json.loads(body)
    
    print(json_response['location']['longitude'])

    pnt = Point(json_response['location']['longitude'], json_response['location']['latitude'])
    

    station = Station.objects.get(location=pnt)

    print(json_response['unit'])

    unit = Unit.objects.get(symbol=json_response['unit'])
    variable = Variable.objects.get(unit=unit)

    new_data = Data(station=station, variable=variable, value=json_response['detectedData'])
    Data.save(new_data)