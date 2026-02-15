import logging

from rest_framework import viewsets
from rest_framework_gis import filters as gis_filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend
from django.db.models import Avg
from django.db.models.functions import TruncDay
from django.utils import timezone

from climatemq.models import Station, Data
from climatemq.serializers import (
    StationSerializer,
    DataSerializer,
    LastDataSerializer,
    StationTableSerializer
)
from climatemq.filters import (
    StationFilter,
    DataFilter

)

logger = logging.getLogger('climatemq.viewsets')

class StationViewSet(viewsets.ReadOnlyModelViewSet):

    bbox_filter_field = "location"
    filter_backends = (
        gis_filters.InBBoxFilter,
    )
    queryset = Station.objects.filter(accepted=True)
    serializer_class = StationSerializer

class LastDataViewSet(viewsets.ReadOnlyModelViewSet):

    bbox_filter_field = "sensor__station__location"
    filter_backends = (
        gis_filters.InBBoxFilter,
    )
    serializer_class = LastDataSerializer
    filterset_fields = ['variable__id']

    def get_queryset(self): 
        variable_id = self.request.GET.get('variable_id','')
        return Data.objects.filter(variable_id=variable_id, sensor__station__accepted=True).order_by('sensor__id','-created_at').distinct('sensor__id')


class StationTableViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Station.objects.filter(accepted=True)
    serializer_class = StationTableSerializer
    filter_backends = [DatatablesFilterBackend]
    filterset_class = StationFilter

class DataViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Data.objects.all()
    serializer_class = DataSerializer
    filter_backends = [DatatablesFilterBackend]
    filterset_class = DataFilter
    filterset_fields = ['sensor__station__id']

    def get_queryset(self):
        return Data.objects.filter(sensor__station__id=self.request.GET.get('station__id', None))

class DataChartViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Data.objects.all()
    serializer_class = DataSerializer

    @action(detail=False, methods=['get'])
    def get_chart_data(self, request):

        labels = []

        end_time = timezone.datetime.today().date() + timezone.timedelta(1)
        start_time = end_time - timezone.timedelta(7)

        for i in range(7):
            day = start_time + timezone.timedelta(i)
            labels.append(day.strftime('%Y-%m-%d'))

        print(labels)
        print(start_time)
        print(end_time)
        filtered_data = Data.objects.filter(sensor__station__id=request.GET.get('station__id', None))
        data_list = filtered_data.values(
            "sensor__station__name", "variable__name", day = TruncDay('created_at')
        ).annotate(avg = Avg('value')).order_by('day').filter(day__range=(start_time, end_time))

        labels = sorted(labels)
        variables = sorted(list(set(data['variable__name'] for data in data_list)))

        dataset = []
        for variable in variables:
            data = []
            for label in labels:
                value = next((data['avg'] for data in data_list 
                              if data['day'].strftime('%Y-%m-%d') == label and data['variable__name'] == variable), 0)
                data.append(value)
            dataset.append({
                'label': variable,
                'data': data,
                'borderColor': f'rgba({hash(variable) % 256}, {hash(variable + "a") % 256}, {hash(variable + "b") % 256}, 1.2)',
                'backgroundColor': f'rgba({hash(variable) % 256}, {hash(variable + "a") % 256}, {hash(variable + "b") % 256}, 0.3)',
                'borderWidth': 1
            })
        
        chartLabel = "my data"
        queryset ={ 
                     "labels":labels, 
                     "chartLabel":chartLabel, 
                     "dataset":dataset, 
             } 
        return Response(queryset) 

