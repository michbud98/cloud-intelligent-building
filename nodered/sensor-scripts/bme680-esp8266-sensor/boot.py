import utime as time
import ubinascii
import machine
from machine import Pin, I2C
import sys
import micropython
import network, urequests, ujson
import esp
from bme680 import *

esp.osdebug(None)
import gc

gc.collect()

ssid = 'SET WIFI NAME'
password = 'SET PASSWORD'
mqtt_server = 'SET NODERED SERVER IP'
# EXAMPLE IP ADDRESS
# nodered_server = '192.168.1.106'

rtc_update_url = f"http://{nodered_server}:1880/datetime"  # rtc_update_url = "https://worldtimeapi.org/api/timezone/Europe/Prague"
nodered_influxdb_url = f"http://{nodered_server}:1880/postSensor"

client_id = ubinascii.hexlify(machine.unique_id())
board_type = "esp8266"
sensor_id = board_type + "-" + client_id.decode("utf-8")
sensor_type = "BME680"

# Message interval in milliseconds needs at least 10000 milliseconds
message_interval_ms = 60000

# True ENABLED | False DISABLED
DEBUG_FILE = False

station = network.WLAN(network.STA_IF)
# Disable ESP8266 Access point interface
access_point = network.WLAN(network.AP_IF)
access_point.active(False)

# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
