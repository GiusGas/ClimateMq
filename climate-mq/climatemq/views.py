from django.shortcuts import render

from climatemq.models import Station, Variable, Data

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