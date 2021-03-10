from django.test import TestCase
from sensor.models import Sensor

# Create your tests here.
class TestAppModels(TestCase):
    
    @classmethod
    def setUp(self):
        self.new = Sensor.objects.create(sensor_id="S1", hostname="sensor", sensor_type="enviro-plus", location="indoors")

    def test_model_str(self):
        self.assertEqual(str(self.new), "S1")

    def test_get_absolute_url(self):
        self.assertEqual(str(self.new.get_absolute_url()), "/sensors/S1")
        