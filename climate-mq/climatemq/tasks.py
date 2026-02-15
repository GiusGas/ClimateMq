# climatemq/tasks.py
from celery import shared_task
from climatemq.utils.prediction_utils import predict_weather_for_station, get_ready_stations
from climatemq.utils.rabbit_utils import RabbitManager

TEMP_CRITICAL = 45
WIND_CRITICAL = 50

@shared_task
def trigger_hourly_predictions():
    """
    1. Finds all stations with the 4 sensors.
    2. Runs the GCC Transformer model for each.
    3. Sends control commands if a catastrophe is predicted.
    """

    stations = get_ready_stations()
    manager = RabbitManager()
    results = []

    print(f"Starting Hourly Prediction for {stations.count()} stations...")

    for station in stations:
        try:
            pred_temp, pred_hum, pred_prec, pred_wind = predict_weather_for_station(station.id)
            results.append(pred_temp)
            results.append(pred_hum)
            results.append(pred_prec)
            results.append(pred_wind)
            
            if pred_temp > TEMP_CRITICAL:
                manager.send_command(station.name, action="SCALE_RATE", value=4.0, variable_name="Temperature")
            if pred_wind > WIND_CRITICAL:
                manager.send_command(station.name, action="SCALE_RATE", value=4.0, variable_name="Wind Speed")

        except Exception as e:
            print(f"Failed to predict for {station.name}: {e}")
            
    return results