import random
import math
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from climatemq.models import Station, Sensor, Data, Variable, Unit

class Command(BaseCommand):
    help = 'Generates 72 hours of dummy weather history for Station 1'

    def handle(self, *args, **options):

        station, _ = Station.objects.get_or_create(id=1)
        
        features = [
            {'name': 'Temperature', 'unit': '°C', 'base': 30, 'var': 5},
            {'name': 'Humidity', 'unit': '%', 'base': 40, 'var': 10},
            {'name': 'Pressure', 'unit': 'hPa', 'base': 1013, 'var': 2},
            {'name': 'Wind Speed', 'unit': 'km/h', 'base': 15, 'var': 10},
        ]

        sensors = {}
        for feat in features:
            unit, _ = Unit.objects.get_or_create(symbol=feat['unit'], defaults={'name': feat['unit']})
            variable, _ = Variable.objects.get_or_create(name=feat['name'], defaults={'symbol': feat['name'][:3], 'unit': unit})
            sensor, _ = Sensor.objects.get_or_create(
                station=station, 
                variable=variable, 
                defaults={'name': f"{feat['name']} Sensor"}
            )
            sensors[feat['name']] = sensor

        now = timezone.now()
        count = 0
        
        print(f"Generating 72-hour history for {station.name}...")
        
        for hour in range(72, 0, -1):
            timestamp = now - timedelta(hours=hour)
            
            time_factor = math.sin((hour / 24) * 2 * math.pi) 

            for feat in features:
                sensor = sensors[feat['name']]
                
                value = feat['base'] + (feat['var'] * time_factor) + random.uniform(-1, 1)
                
                if feat['name'] == 'Wind Speed' and random.random() > 0.95:
                    value += 20
                
                Data.objects.create(
                    sensor=sensor,
                    variable=sensor.variable,
                    value=round(value, 2),
                    created_at=timestamp
                )
                count += 1

        print(f"Successfully created {count} data points. Ready for Transformer Inference.")