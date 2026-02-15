import pika
import json
from django.conf import settings

EXCHANGE = "data"

class RabbitManager:
    _instance = None
    _connection = None
    _publish_channel = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitManager, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        if self._connection is None or self._connection.is_closed:
            params = pika.ConnectionParameters(
                host='rabbitmq', 
                port=5672,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self._connection = pika.BlockingConnection(params)
        return self._connection

    def get_publish_channel(self):
        """Returns a dedicated channel for sending commands."""
        if self._publish_channel is None or self._publish_channel.is_closed:
            conn = self.get_connection()
            self._publish_channel = conn.channel()

            self._publish_channel.exchange_declare(
                exchange=EXCHANGE,
                exchange_type='topic', 
                durable=True
            )
        return self._publish_channel

    def send_command(self, station_name, action, value, variable_name):
        """
        The centralized command sender used by both Consumer and Predictor.
        """
        try:
            channel = self.get_publish_channel()
            payload = json.dumps({
                "action": action, 
                "value": value
            })
            
            routing_key = f'station.control.{station_name}.{variable_name}'
            
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=payload,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(f" [Execute] Sent {action}={value} to {variable_name} Sensor of Station {station_name}")
        except Exception as e:
            print(f" [MQ] Error sending command: {e}")
            self._publish_channel = None
   