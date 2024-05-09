import logging

from rest_framework import viewsets
from rest_framework_gis import filters

from climatemq.models import Station
from climatemq.serializers import (
    StationSerializer,
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

    def list(self, request, *args, **kwargs):
        read_temperature()
        return super.list(self, request, *args, **kwargs)
