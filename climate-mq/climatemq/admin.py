from django.contrib.gis import admin

from climatemq.models import Station, Unit, Variable, Sensor, Data

admin.site.site_url = "/climatemq/map/"

@admin.register(Station)
class StationAdmin(admin.GISModelAdmin):
    list_display = ("name", "location", "accepted")
    list_filter = ["accepted"]

@admin.register(Unit)
class UnitAdmin(admin.GISModelAdmin):
    list_display = ("name", "symbol")

@admin.register(Variable)
class VariableAdmin(admin.GISModelAdmin):
    list_display = ("symbol", "name", "unit", "precision", "scale")

@admin.register(Sensor)
class SensorAdmin(admin.GISModelAdmin):
    list_display = ("name", "station")

@admin.register(Data)
class DataAdmin(admin.GISModelAdmin):
    list_display = ("value", "variable", "station", "created_at")
