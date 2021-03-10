from django.test import TestCase
from django.urls import reverse, resolve
from sensor.models import Sensor
from sensor.views import (sensor_list_view, sensor_create_view,
 sensor_remove_view, sensor_detail_view, sensor_update_view)

class TestURLs(TestCase):
    def setUp(self):
        self.new = Sensor.objects.create(sensor_id="S4", hostname="sensor4", sensor_type="BME680", location="outdoors")

    def test_sensor_list_resolve(self):
        url = reverse("sensor_list")
        self.assertEqual(resolve(url).func, sensor_list_view)

    def test_sensor_detail_resolve(self):
        url = reverse("sensor_detail", kwargs={"sensor_id": self.new.sensor_id})
        self.assertEqual(resolve(url).func, sensor_detail_view)
    
    def test_sensor_create_resolve(self):
        url = reverse("sensor_create", kwargs={"sensor_id": self.new.sensor_id, "hostname": self.new.hostname, 
        "sensor_type": self.new.sensor_type})
        self.assertEqual(resolve(url).func, sensor_create_view)

