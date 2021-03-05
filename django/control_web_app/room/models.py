from django.db import models
from django.urls import reverse

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=30)

    def __str__(self):
        return self.room_name