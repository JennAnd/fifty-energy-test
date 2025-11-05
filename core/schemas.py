# Schemas define how data is structured when sent to or sent from the API
from ninja import Schema
from datetime import datetime
from typing import Optional

# Base schema for common sensor fields
class SensorBase(Schema):
    name: str
    type: str

# Used when creating a new sensor (POST)
class SensorCreate(SensorBase):
    pass

# Used when returning sensor data in API responses (GET)
class SensorOut(SensorBase):
    id: int
    created_at: datetime

# Base schema for reading data like temperature and humidity
class ReadingBase(Schema):
    temperature: float
    humidity: Optional[float] = None
    timestamp: datetime

# Used when adding a new reading for a sensor (POST)
class ReadingCreate(ReadingBase):
    pass # sensor_id comes from url not the body

# Used when returning readings from the API (GET)
class ReadingOut(ReadingBase):
    id: int