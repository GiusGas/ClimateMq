from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework import serializers
from climatemq.models import Data

from climatemq.models import Station


class StationSerializer(
    GeoFeatureModelSerializer
):
    class Meta:
        fields = ("id", "name", "consuming")
        geo_field = "location"
        model = Station

class DataSerializer(serializers.ModelSerializer):

    unit_symbol = serializers.CharField(source='variable.unit.symbol')
    variable_name = serializers.CharField(source='variable.name')

    class Meta:
        model = Data
        fields = ['id', 'value', 'unit_symbol', 'variable_name']
