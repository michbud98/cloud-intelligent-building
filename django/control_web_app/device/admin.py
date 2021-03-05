from django.contrib import admin

# Register your models here.
from .models import Device, Thermo_head, Sunblind

admin.site.register(Device)
admin.site.register(Thermo_head)
admin.site.register(Sunblind)