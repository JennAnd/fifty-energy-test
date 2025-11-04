# Custom Django management command to add one test user and 5 sensors
# Create demo readings for each sensor 
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Sensor
import random
from datetime import timedelta
from django.utils import timezone
from core.models import Reading

# List of sensors to add for the test user
SENSORS = [
    ("device-001", "EnviroSense"),
    ("device-002", "ClimaTrack"),
    ("device-003", "AeroMonitor"),
    ("device-004", "HydroTerm"),
    ("device-005", "EcoStat"),
]

# Custom command for adding test data (run with: python manage.py seed_data)
class Command(BaseCommand):
    help = "Creates test user, five sensors and five readings to each sensor."

    def handle(self, *args, **opts):
        #Create or get a user with the given username, prevents duplicate users
        user, created = User.objects.get_or_create(
            username="jennifer_test", defaults={"email": "jennifer@test.com"}
        )
        if created:
            user.set_password("jennifer123")
            user.save()

        # Add all sensors to the user and skip if already exist
        for name, model in SENSORS: # "model" because not possible to use type
            Sensor.objects.get_or_create(
                owner=user,
                name=name,
                defaults={"type": model,}
            )
        
        # Get the current time
        now = timezone.now()

        # Loop through all sensors owned by the user
        for sensor in Sensor.objects.filter(owner=user):
            #Create 5 readings per sensor, 1 hour apart
            for i in range(5): 
                ts = now - timedelta(hours=i) 
                # Create a reading with random temperature and humidity
                Reading.objects.get_or_create(
                    sensor=sensor,
                    timestamp=ts,
                    defaults={
                        "temperature": round(random.uniform(15.0, 25.0), 1), # Round to 1 decimal
                        "humidity": round(random.uniform(35.0, 60.0), 1),
                    }
                )
        # Print a success message in the terminal when seeding is done
        self.stdout.write(self.style.SUCCESS("Seed OK! Created Jennifer's test user, 5 sensors and 5 readings per sensor."))