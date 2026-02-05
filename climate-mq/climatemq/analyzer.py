from django.contrib.gis.measure import D

from climatemq.models import Station, Variable, Goal

class Analyzer:
    def __init__(self, type):
        self.type = type

    def analyze_and_plan(self, station, variable, latest_value):
        # Find goals for this variable
        goals = Goal.objects.filter(variable=variable, is_active=True)
        
        for goal in goals:
            # Simple threshold check
            if (goal.operator == '>' and latest_value > goal.threshold) or \
            (goal.operator == '<' and latest_value < goal.threshold):
                
                # GIS Rule: Apply this to all stations within 5km (Spatial Standard)
                nearby_stations = Station.objects.filter(
                    location__distance_lte=(station.location, D(km=5))
                )
                
                for s in nearby_stations:
                    self.execute_action(s, goal.action)
