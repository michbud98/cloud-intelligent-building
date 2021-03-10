from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from sensor.models import Sensor
from room.models import Room


class TestViews(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.new = Sensor.objects.create(sensor_id="S2", hostname="sensor2", sensor_type="1-wire", location="boiler")
        self.new_room = Room.objects.create(id=1,room_name="test_room")
    
    def test_sensor_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse("sensor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sensor_list.html")

    def test_sensor_list_login_redirection(self):
        response = self.client.get(reverse("sensor_list"), follow=True)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_sensor_create_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse("sensor_create", args=["S3", "sensor3", "STH22"])
        response = self.client.post(url, {
            "location": "indoors",
            "room": 1
        })

        sensor = Sensor.objects.get(sensor_id="S3")
        self.assertEquals(str(sensor), "S3")
        self.assertEquals(sensor.location, "indoors")
        self.assertEquals(sensor.room.id, self.new_room.id)