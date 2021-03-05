from django.db import models
from django.urls import reverse
from room.models import Room

# Create your models here.
class Device(models.Model):
    DEVICE_TYPES = (
        ('sunblind', 'sunblind'),
        ('thermo_head', 'thermostatic head'),
    )
    device_id = models.CharField(max_length=30, unique=True)
    device_type = models.CharField(max_length=30, choices=DEVICE_TYPES)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    last_request = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.device_id

    class Meta:
        ordering = ['device_id']

class Thermo_head(Device):
    set_heat_value = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    last_requested_heat_value = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

class Sunblind(Device):
    set_open_value = models.BooleanField(default=False)
    last_requested_open_value = models.BooleanField(default=False)