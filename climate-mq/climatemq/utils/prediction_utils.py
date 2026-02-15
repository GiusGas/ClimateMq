import torch
import numpy as np
import pandas as pd
from django.db.models import Count
from django.utils import timezone

from climatemq.models import Station, Sensor, Data, SensorGoal
from climatemq.ml_engine import get_weather_model

FEATURE_NAMES = ['temperature_2m', 'relative_humidity_2m', 'precipitation', 'wind_speed_10m']

VAR_MAP = {
    'temperature_2m': 'Temperature',
    'relative_humidity_2m': 'Humidity',
    'precipitation': 'Precipitation',
    'wind_speed_10m': 'Wind Speed'
}

def get_recent_data(station_id):
    """
    Fetches last 72 hours of data and pivots it into shape (72, 4)
    """
    data_matrix = []
    
    for feature_col in FEATURE_NAMES:
        db_var_name = VAR_MAP[feature_col]
        
        sensor = Sensor.objects.filter(station_id=station_id, variable__name=db_var_name).first()
        if not sensor:
            print(f"Missing sensor for {db_var_name}")
            return None
            
        records = list(Data.objects.filter(sensor=sensor).order_by('-created_at')[:72])
        
        if len(records) < 72:
            print(f"Not enough data for {db_var_name}. Need 72, got {len(records)}.")
            return None
            
        records.sort(key=lambda x: x.created_at)
        values = [r.value for r in records]
        data_matrix.append(values)
    
    np_matrix = np.array(data_matrix).T
    return np_matrix

def get_ready_stations():
    """
    Returns a QuerySet of stations that have ALL 4 required sensors.
    """
    required_db_vars = list(VAR_MAP.values())
    
    return Station.objects.filter(
        sensor__variable__name__in=required_db_vars
    ).annotate(
        sensor_count=Count('sensor__variable__name', distinct=True)
    ).filter(
        sensor_count=4
    )

def predict_weather_for_station(station_id):

    model, scaler = get_weather_model()
    if model is None:
        print("Model not loaded.")
        return None
    
    raw_data = get_recent_data(station_id)
    if raw_data is None:
        return None

    df_input = pd.DataFrame(raw_data, columns=FEATURE_NAMES)
    
    try:
        norm_data = scaler.transform(df_input)
    except Exception as e:
        print(f"Scaling Error: {e}")
        return None
    
    input_tensor = torch.tensor(norm_data, dtype=torch.float32).unsqueeze(0)
    

    with torch.no_grad():
        prediction_norm = model(input_tensor)
        pred_np = prediction_norm.cpu().numpy()
    
    last_input = norm_data[-1, :].copy()
    target_idx = next(i for i, f in enumerate(FEATURE_NAMES) if 'temp' in f.lower())
    
    new_step_scaled = last_input
    new_step_scaled[target_idx] = pred_np.item()

    try:
        pred_df = new_step_scaled.reshape(1, len(FEATURE_NAMES))
        prediction_real = scaler.inverse_transform(pred_df)[0]
    except Exception as e:
        print(f"Scaling Error: {e}")
        return None

    pred_temp = prediction_real[0]
    pred_hum  = prediction_real[1]
    pred_prec = prediction_real[2]
    pred_wind = prediction_real[3]
    
    print("\n🔮 PREDICTION FOR NEXT HOUR:")
    print(f"  Temp: {pred_temp:.2f} °C")
    print(f"  Hum:  {pred_hum:.2f} %")
    print(f"  Rain: {pred_prec:.2f} mm")
    print(f"  Wind: {pred_wind:.2f} km/h")
    
    now = timezone.now()
    temp_query = {"station_id": station_id, "variable__name": VAR_MAP['temperature_2m']}
    hum_query  = {"station_id": station_id, "variable__name": VAR_MAP['relative_humidity_2m']}
    prec_query = {"station_id": station_id, "variable__name": VAR_MAP['precipitation']}
    wind_query = {"station_id": station_id, "variable__name": VAR_MAP['wind_speed_10m']}

    sensor_temp = Sensor.objects.get(**temp_query)
    sensor_temp.predicted_value = pred_temp
    sensor_temp.predicted_at = now
    sensor_temp.save()

    sensor_hum = Sensor.objects.get(**hum_query)
    sensor_hum.predicted_value = pred_hum
    sensor_hum.predicted_at = now
    sensor_hum.save()

    sensor_prec = Sensor.objects.get(**prec_query)
    sensor_prec.predicted_value = pred_prec
    sensor_prec.predicted_at = now
    sensor_prec.save()

    sensor_wind = Sensor.objects.get(**wind_query)
    sensor_wind.predicted_value = pred_wind
    sensor_wind.predicted_at = now
    sensor_wind.save()

    SensorGoal.objects.get_or_create(sensor=sensor_temp)
    SensorGoal.objects.get_or_create(sensor=sensor_hum)
    SensorGoal.objects.get_or_create(sensor=sensor_prec)
    SensorGoal.objects.get_or_create(sensor=sensor_wind)

    return pred_temp, pred_hum, pred_prec, pred_wind