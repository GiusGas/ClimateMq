from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F

from climatemq.models import *

EXCHANGE = 'data'

def apply_battery_strategy(station, variable, battery):
    """
    Manages Lifecycle based on energy.
    Uses SCALING factors (Percentage) rather than absolute rates.
    1.0 = 100% (Normal), 0.5 = 50% (Slow), 2.0 = 200% (Fast)
    """
    commands = []
    neighbor = get_nearest_neighbor(station, variable)

    if battery < 20.0:
        # CRITICAL: shut down self, scale neighbor
        commands.append((station.name, 'SWITCH', 'OFF'))
        Sensor.objects.filter(station=station, variable=variable).update(status='INACTIVE')
        if neighbor:
            commands.append((neighbor.name, 'SCALE_RATE', 2.0))

    elif battery < 40.0:
        # LOW: throttle self, help neighbor
        commands.append((station.name, 'SCALE_RATE', 0.5))
        if neighbor:
            commands.append((neighbor.name, 'SCALE_RATE', 1.5))

    return commands

def apply_goal_strategy(station, variable, value):
    """
    Checks User-defined thresholds (Goals).
    If violated, alerts neighborhood.
    """
    commands = []
    goals = Goal.objects.filter(variable=variable, is_active=True)

    for goal in goals:
        violated = False
        if goal.operator == '>' and value > goal.threshold:
            violated = True
        elif goal.operator == '<' and value < goal.threshold:
            violated = True
        elif goal.operator == '==' and value == goal.threshold:
            violated = True

        if violated:
            print(f" [Plan] GOAL VIOLATED: {goal.name}. Alerting Neighborhood.")
            nearby = Station.objects.filter(
                sensor__variable__name=variable.name,
                sensor__status='ACTIVE',
                location__distance_lte=(station.location, D(km=5))
            )

            for s in nearby:
                if goal.action:
                    commands.append((s.name, goal.action.command_key, goal.action.value))

    return commands

def get_nearest_neighbor(station, variable):
    """Finds the closest station to transfer load to."""
    return Station.objects.exclude(id=station.id) \
        .filter(
            sensor__variable__name=variable.name,
            sensor__status='ACTIVE'
        ) \
        .annotate(distance=Distance('location', station.location)) \
        .annotate(battery_distance=F('sensor__battery_level') - F('distance')) \
        .order_by('-battery_distance') \
        .first()