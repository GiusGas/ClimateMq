
from django.core.management.base import BaseCommand
from climatemq.consumer import Consumer
class Command(BaseCommand):
    help = 'Launches Consumer for climate message : RaabitMQ'
    def handle(self, *args, **options):
        td = Consumer()
        td.start()
        self.stdout.write("Started Consumer Thread")