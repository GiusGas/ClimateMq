from django.shortcuts import render
from django.db.models import Min, Max, Count
from django.utils import timezone

from climatemq.models import Station, Variable, Data, Sensor

from django.views.generic.base import (
    TemplateView,
    View
)

class StationsMapView(TemplateView):
    template_name = "map.html"

    def get(self, request, *args, **kwargs):
        variable_list = Variable.objects.all()

        return render(request, self.template_name, {"variable_list":variable_list})

class StationsListView(View):
    template_name = "station_list.html"

    def get(self, request, *args, **kwargs):
        station_list = get_station_list()
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
        return render(request, self.template_name, {"data_list":data_list, "station_list":station_list})

def get_station_list():
    return Station.objects.filter(accepted=True)

def get_data_list(station_id):
    return Data.objects.filter(station_id=station_id)

def monitoring_view(request):
    now = timezone.now()
    today = now.date()

    total_stations = Station.objects.count()
    active_sensors_count = Sensor.objects.filter(status='ACTIVE').count()
    inactive_sensors_count = Sensor.objects.filter(status='INACTIVE').count()
    broken_sensors_count = Sensor.objects.filter(status='BROKEN').count()

    sensors_list = []
    sensors = Sensor.objects.select_related('station', 'variable').all()
    
    for sensor in sensors:

        stats = Data.objects.filter(
            sensor=sensor, 
            created_at__date=today
        ).aggregate(
            first_msg=Min('created_at'),
            last_msg=Max('created_at'),
            count=Count('id')
        )

        count = stats['count']
        sending_rate = 0

        if count > 1 and stats['first_msg'] and stats['last_msg']:
            duration = (stats['last_msg'] - stats['first_msg']).total_seconds()
            sending_rate = round(duration / (count - 1), 2)

        sensors_list.append({
            'name': f"{sensor.station.name} - {sensor.name}",
            'status': sensor.status,
            'battery': sensor.battery_level,
            'total_today': count,
            'rate': sending_rate,
            'predicted': sensor.predicted_value,
            'predicted_at': sensor.predicted_at
        })

    context = {
        'total_stations': total_stations,
        'active_sensors': active_sensors_count,
        'inactive_sensors': inactive_sensors_count,
        'broken_sensors': broken_sensors_count,
        'sensors': sensors_list,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'monitoring_fragment.html', context)
    
    return render(request, 'monitoring.html', context)