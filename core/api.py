# Router file for the core app
from ninja import Router
from .models import Sensor
from typing import List
from .schemas import SensorCreate, SensorOut
from .auth_bearer import TokenAuth # Import TokenAuth class to protect endpoints

# Create a router to handle API endpoints related to sensors
router = Router()

# Endpoint to get a list of all sensors from the database
@router.get("/sensors", response=List[SensorOut], auth=TokenAuth()) # Requires valid endpoint to access this endpoint
def list_sensors(request):
    sensors = Sensor.objects.filter(owner=request.auth) # Only show sensors that belongs to logged-in user
    return sensors

# Create a new sensor using data from the request
@router.post("/sensors", response=SensorOut, auth=TokenAuth())
def create_sensor(request, data: SensorCreate):
    sensor = Sensor.objects.create(**data.dict(), owner=request.auth) # Creates a new sensor using the data from the schema

    return sensor

