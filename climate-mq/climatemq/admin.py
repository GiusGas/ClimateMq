from django.contrib.gis import admin

from climatemq.models import Station, Unit, Variable, Sensor, Data, ActuatorAction, Goal, SensorGoal

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
    list_display = ("name", "station", "variable", "status", "battery_level")

@admin.register(Data)
class DataAdmin(admin.GISModelAdmin):
    list_display = ("value", "variable", "sensor", "created_at")

@admin.register(ActuatorAction)
class ActuatorActionAdmin(admin.GISModelAdmin):
    list_display = ("name", "command_key", "value")

@admin.register(Goal)
class GoalAdmin(admin.GISModelAdmin):
    list_display = ("name", "variable", "operator", "threshold", "action", "is_active")

@admin.register(SensorGoal)
class SensorGoalAdmin(admin.GISModelAdmin):
    list_display = ("sensor", "max_variance", "consecutive_anomalies", "is_broken")
