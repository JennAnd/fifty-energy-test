from django.db import models
from django.contrib.auth.models import User

# Model that defines a sensor owned by a user, including its name, type and creation date
class Sensor(models.Model):
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # Links the sensor to the user who owns it
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # Model that saves measurements for each sensor with temperature, humidity and time
class Reading(models.Model):
    sensor = models.ForeignKey("core.Sensor", on_delete=models.CASCADE, related_name="readings") # Connects each reading to its sensor
    temperature = models.FloatField()
    humidity = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ["timestamp"]
        unique_together = ("sensor", "timestamp")

        def __str__(self):
            return f"{self.sensor.name} - {self.timestamp}"   
