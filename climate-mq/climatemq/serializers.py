from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework import serializers
from climatemq.models import Data

from climatemq.models import Station


class StationSerializer(
    GeoFeatureModelSerializer
):
    class Meta:
        fields = ("id", "name", "accepted")
        geo_field = "location"
        model = Station

class LastDataSerializer(GeoFeatureModelSerializer):

    station_location = GeometryField(source='station.location')
    unit_symbol = serializers.CharField(source='variable.unit.symbol')
    station_name = serializers.CharField(source='station.name')
    class Meta:
        fields = ("value", "unit_symbol", "station_name")
        geo_field = "station_location"
        model = Data

class DataSerializer(serializers.ModelSerializer):

    unit_symbol = serializers.CharField(source='variable.unit.symbol')
    variable_name = serializers.CharField(source='variable.name')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=None, default_timezone=None)

    class Meta:
        model = Data
        fields = ['id', 'value', 'unit_symbol', 'variable_name', 'created_at']

class DataAvgSerializer(serializers.ModelSerializer):

    avg = serializers.FloatField()
    unit_symbol = serializers.CharField()
    variable_name = serializers.CharField()
    day = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    station__name = serializers.CharField()

    class Meta:
        fields = ['station__name', 'unit_symbol', 'variable_name', 'day', 'avg']

class StationTableSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    class Meta:
        fields = ["id", "name", "accepted", "latitude", "longitude"]
        model = Station

    def get_longitude(self, obj):
        return obj.location.x

    def get_latitude(self, obj):
        return obj.location.y
