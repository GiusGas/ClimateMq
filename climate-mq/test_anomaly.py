import pika
import json
import time
import sys

def send_anomaly_test():
    """
    Sends intentionally incorrect data for Rome_Station_0_Temperature
    to test if the SensorGoal logic triggers a rate increase and eventual shutdown.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare the same data exchange used in your project
    channel.exchange_declare(exchange='data', exchange_type='topic', durable=True)

    station_name = "Rome_Station_0"
    variable = "Temperature"
    
    # We send 3 values that are clearly 'wrong' (e.g., 99°C or -50°C)
    # Your model likely predicts ~20-30°C, so these will trigger the >10.0 variance.
    test_values = [95.5, 98.2, 105.0, 25.0] # 3 anomalies + 1 'normal' value
    
    print(f"🚀 Starting Anomaly Test for {station_name}_{variable}...")

    for i, val in enumerate(test_values):
        payload = {
            "station": {
                "name": station_name,
                "location": {"longitude": 12.0, "latitude": 41.0},
                "username": station_name, 
                "key": station_name
            },
            "unit": "°C",
            "variable": variable,
            "detectedData": val,
            "battery": 85.0
        }

        routing_key = 'sensor.detected'
        channel.basic_publish(
            exchange='data', 
            routing_key=routing_key, 
            body=json.dumps(payload)
        )
        
        print(f"[{i+1}/4] Sent Value: {val}°C")
        
        if i < 2:
            print("   -> Expected: Strike recorded, Rate increased to 1s.")
        elif i == 2:
            print("   -> Expected: STRIKE 3! Sensor should SHUT DOWN.")
        else:
            print("   -> Expected: This value should be REJECTED because sensor is now inactive.")

        # Wait a bit for the backend to process and update the Goal
        time.sleep(2)

    connection.close()
    print("\n Test sequence complete.")
    print("1. Data table should NOT contain the values 95.5, 98.2, or 105.0.")
    print("2. Sensor Rome_Station_0 should have is_active=False.")
    print("3. SensorGoal should have consecutive_anomalies=3.")

if __name__ == "__main__":
    send_anomaly_test()