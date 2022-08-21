
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
from machine import Pin, I2C
import sys
import micropython
import network
import esp
from bme680 import *

esp.osdebug(None)
import gc
gc.collect()


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

message_interval_ms = 60000
DEBUG_FILE = 1

station = network.WLAN(network.STA_IF)
#Disable ESP8266 Access point interface
access_point = network.WLAN(network.AP_IF)
access_point.active(False)
 
# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)