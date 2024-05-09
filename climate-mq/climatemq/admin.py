from django.contrib.gis import admin

from climatemq.models import Station


@admin.register(Station)
class StationAdmin(admin.GISModelAdmin):
    list_display = ("name", "location")
