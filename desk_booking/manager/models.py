from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length = 64)
    city = models.CharField(max_length = 64)
    country = models.CharField(max_length= 64)

    def __str__(self):
        return f'{self.name} {self.city} {self.country}'

class Floor(models.Model):
    name = models.CharField(max_length = 64)
    map = models.ImageField(null = False, blank = False, upload_to = "maps/")
    parent_location = models.ForeignKey('Location', on_delete = models.CASCADE)
    
    def __str__(self):
        return f"Floor {self.name} {self.parent_location}"

class Desk(models.Model):
    left_up_x = models.IntegerField(blank = False, null = False)
    left_up_y = models.IntegerField(blank = False, null = False)
    right_down_x = models.IntegerField(blank = False, null = False)
    right_down_y = models.IntegerField(blank = False, null = False)
    parent_floor = models.ForeignKey("Floor", on_delete = models.CASCADE)
    
    def __str__(self):
        return f"Desk {self.id} {self.parent_floor}"

