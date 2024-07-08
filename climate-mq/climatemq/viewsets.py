import logging

from rest_framework import viewsets
from rest_framework_gis import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_serverside_datatable.views import ServerSideDatatableView

from climatemq.models import Station, Data
from climatemq.serializers import (
    StationSerializer,
    DataSerializer,
)

from climatemq.views import read_temperature

logger = logging.getLogger('climatemq.urls')

class StationViewSet(viewsets.ReadOnlyModelViewSet):

    bbox_filter_field = "location"
    filter_backends = (
        filters.InBBoxFilter,
    )
    queryset = Station.objects.all()
    serializer_class = StationSerializer

#    def read(self, request, *args, **kwargs):
#        read_temperature()

class DataViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Data.objects.all()
    serializer_class = DataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station__id']

class DataTableSet(ServerSideDatatableView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station__id']
    columns = ['id', 'value', 'unit_symbol', 'variable_name']
