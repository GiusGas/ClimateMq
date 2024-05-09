from rest_framework_gis.serializers import GeoFeatureModelSerializer

from climatemq.models import Station


class StationSerializer(
    GeoFeatureModelSerializer
):
    class Meta:
        fields = ("id", "name")
        geo_field = "location"
        model = Station