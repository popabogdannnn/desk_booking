from django.contrib import admin
from .models import Location, Floor, Desk
# Register your models here.

admin.site.register(Location)
admin.site.register(Floor)
admin.site.register(Desk)