from django.core.management.base import BaseCommand
from climatemq.tasks import trigger_hourly_predictions

class Command(BaseCommand):
    help = 'Manually triggers the weather prediction MAPE-K loop'

    def handle(self, *args, **options):
        self.stdout.write("Manually triggering prediction task...")
        trigger_hourly_predictions.apply() #to run it right here in this terminal
        #trigger_hourly_predictions.delay() #to do it in the background
        self.stdout.write(self.style.SUCCESS("Task execution finished."))