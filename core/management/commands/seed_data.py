# Custom Django management command to add one test user and 5 sensors
# Create demo readings for each sensor 
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Sensor
from core.models import Reading
import csv
from pathlib import Path
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError

# List of sensors to add for the test user
SENSORS = [
    ("device-001", "EnviroSense"),
    ("device-002", "ClimaTrack"),
    ("device-003", "AeroMonitor"),
    ("device-004", "HydroTherm"),
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

        csv_path = Path(__file__).resolve().parent.parent.parent.parent / "sensor_readings_wide.csv"

        # Fail if the file does not exist
        if not csv_path.exists():
                self.stderr.write(f"CSV not found: {csv_path}")
                return

        created_count = 0

        # Open csv and read rows using the header name
        with csv_path.open(newline="") as f:
            reader = csv.DictReader(f)  # expects: timestamp, device_id, temperature, humidity
            for row in reader:
                device = row["device_id"]  # Match device name to Sensor.name

                try:
                    sensor = Sensor.objects.get(name=device, owner=user)
                except Sensor.DoesNotExist:
                    continue  # skip unknown devices

                ts = parse_datetime(row["timestamp"])
                if not ts:
                    continue  # skip bad timestamps

                # Create a Reading linked to the sensor
                try:
                    Reading.objects.create(
                        sensor=sensor,
                        temperature=float(row["temperature"]),
                        humidity=float(row["humidity"]),
                        timestamp=ts,
                    )
                    created_count += 1
                except IntegrityError:
                    # Skip duplicate readings for same (sensor, timestamp)
                    continue

     
        # Print a success message in the terminal when seeding is done
        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created_count} readings added from CSV"))