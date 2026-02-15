from django.apps import AppConfig

class ClimatemqConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "climatemq"

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN'):
            from .ml_engine import get_weather_model
            print("Pre-loading model on startup...")
            get_weather_model()

            from climatemq.consumer import Consumer
            print("Model loaded. Starting RabbitMQ Consumer thread...")
            thread = Consumer()
            thread.daemon = True
            thread.start()
