from django.contrib import admin
from .models import Location, Floor, Desk, Booking
# Register your models here.

admin.site.register(Location)
admin.site.register(Floor)
admin.site.register(Desk)
admin.site.register(Booking)