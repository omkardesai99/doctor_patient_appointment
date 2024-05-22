from django.core.management.base import BaseCommand
from datetime import time, timedelta, datetime
from appointments.models import TimeSlot


class Command(BaseCommand):
    help = "Populate TimeSlot model with 30 minute intervals from 9 AM to 9 PM"

    def handle(self, *args, **kwargs):
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("21:00", "%H:%M")
        current_time = start_time

        while current_time < end_time:
            TimeSlot.objects.get_or_create(
                start_time=current_time.time(),
                end_time=(current_time + timedelta(minutes=30)).time(),
            )
            current_time += timedelta(minutes=30)

        self.stdout.write(self.style.SUCCESS("Successfully populated TimeSlot model"))
