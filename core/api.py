# Router file for the core app
from ninja import Router
from .models import Sensor
from typing import List
from .schemas import SensorCreate, SensorOut

# Create a router to handle API endpoints related to sensors
router = Router()

# Endpoint to get a list of all sensors from the database
@router.get("/sensors", response=List[SensorOut])
def list_sensors(request):
    sensors = Sensor.objects.all()
    return sensors

# Create a new sensor using data from the request
@router.post("/sensors", response=SensorOut)
def create_sensor(request, data: SensorCreate):
    sensor = Sensor.objects.create(**data.dict()) # Turns the data schema into fields when creating a new sensor
    return sensor

