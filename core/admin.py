from django.contrib import admin
from .models import Sensor, Reading

# Make Sensor & Reading models visible in the admin page
admin.site.register(Sensor)
admin.site.register(Reading)
