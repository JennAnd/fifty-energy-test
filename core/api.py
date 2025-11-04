# Router file for the core app
from ninja import Router
from .models import Sensor
from typing import List
from .schemas import SensorCreate, SensorOut
# from .auth_bearer import TokenAuth # Import TokenAuth class to protect endpoints
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token
from django.db.models import Q # Filtering with multiple fields
from typing import Optional
from ninja.pagination import paginate, PageNumberPagination 

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

