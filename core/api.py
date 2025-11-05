# Router file for the core app
from ninja import Router
from .models import Sensor, Reading
from typing import List
from .schemas import SensorCreate, SensorOut, ReadingCreate, ReadingOut
# from .auth_bearer import TokenAuth # Import TokenAuth class to protect endpoints
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token
from django.db.models import Q # Filtering with multiple fields
from typing import Optional
from ninja.pagination import paginate, PageNumberPagination 
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime


# Checks if the token belongs to a real user
class TokenAuth(HttpBearer):
    def authenticate(self, request, token): # Runs when someone sends a request with a token
        try:
            user = Token.objects.get(key=token).user
            return user # If correct token return the user
        except Token.DoesNotExist:
            return None
    
# Create a router to handle API endpoints related to sensors
router = Router()

# Endpoint to get a list of all sensors from the database
@router.get("/sensors", response=List[SensorOut], auth=TokenAuth()) # Requires valid endpoint to access this endpoint
@paginate(PageNumberPagination, page_size=10) # Splits results to pages
def list_sensors(request, q: Optional[str]= None):
    sensors = Sensor.objects.filter(owner=request.auth) # Only show sensors that belongs to logged-in user
    if q:
        sensors = sensors.filter( # Filter sensors by name or type
            Q(name__icontains=q) | Q(type__icontains=q)
        )
    return sensors

# Logged-in user can create a new sensor in the database
@router.post("/sensors", response=SensorOut, auth=TokenAuth())
def create_sensor(request, data: SensorCreate):
    sensor = Sensor.objects.create(**data.dict(), owner=request.auth) # Creates a new sensor using the data from the schema

    return sensor

# Create router for all reading endpoints
readings_router = Router(auth=TokenAuth())

# Get endpoint to list readings for a specific sensor
@readings_router.get("/sensors/{sensor_id}/readings", response=List[ReadingOut])
def list_readings(
    request,
    sensor_id: int,
    timestamp_from: Optional[str] = None,
    timestamp_to: Optional[str] = None,

):
    # Get sensor that belongs to logged-in user
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)

    # Get readings that belong to this sensor
    readings = Reading.objects.filter(sensor=sensor)

    if timestamp_from:
        dt_from = parse_datetime(timestamp_from)
        if dt_from:
            readings = readings.filter(timestamp__gte=dt_from)
    if timestamp_to:
        dt_to = parse_datetime(timestamp_to)
        if dt_to:
            readings = readings.filter(timestamp__lte=dt_to)

    # Return readings ordered ny newest first
    return readings.order_by("-timestamp")

# Post endpoint to create a new reading for a specific sensor
@readings_router.post("/sensors/{sensor_id}/readings", response=ReadingOut)
def create_reading(request, sensor_id: int, data: ReadingCreate):

    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)

    # Create a new reading in the database using data from the request body
    reading = Reading.objects.create(
        sensor=sensor,
        temperature=data.temperature,
        humidity=data.humidity,
        timestamp=data.timestamp,
    )

    return reading


