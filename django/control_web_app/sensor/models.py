from django.db import models
from django.urls import reverse
from room.models import Room

# Create your models here.
class Sensor(models.Model):
    sensor_id = models.CharField(max_length=30, unique=True)
    hostname = models.CharField(max_length=30, blank=True, null=True)
    sensor_type = models.CharField(max_length=20)
    location = models.CharField(max_length=10)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.sensor_id

    def get_absolute_url(self):
        return reverse("sensor_detail", kwargs={"sensor_id": self.sensor_id})