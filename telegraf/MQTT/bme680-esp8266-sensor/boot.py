
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from bme680 import *
from machine import Pin, I2C

esp.osdebug(None)
import gc
gc.collect()

led = Pin(2, Pin.OUT)
led.value(1)

ssid = 'SET WIFI NAME'
password = 'SET PASSWORD'
mqtt_server = 'SET MQTT SERVER IP'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.106'

client_id = ubinascii.hexlify(machine.unique_id())
board_type = "esp8266"
sensor_id = board_type + "-" + client_id.decode("utf-8")
sensor_type = "BME680"
room = ""

# Topics to publish
pub_values = b'sensor/values'
pub_sensor_status = b'sensor/status'

# Topics to subscribe
sub_room = b'sensor/room'

last_message = 0
message_interval = 60
burn_time = 600

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')