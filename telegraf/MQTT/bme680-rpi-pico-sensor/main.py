import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
from bme680 import *
from machine import Pin, I2C

import gc
gc.collect()


ssid = 'SET WIFI NAME'
password = 'SET PASSWORD'
mqtt_server = 'SET MQTT SERVER IP'
# EXAMPLE IP ADDRESS
# mqtt_server = '192.168.1.106'

client_id = ubinascii.hexlify(machine.unique_id())
board_type = "pico"
sensor_id = board_type + "-" + client_id.decode("utf-8")
sensor_type = "BME680"
room = ""

# Topics to publish
pub_values = b'sensor/values'
pub_sensor_status = b'sensor/status'

# Topics to subscribe
sub_room = b'sensor/room'

message_interval_ms = 60000

station = network.WLAN(network.STA_IF)
station.active(True)
# Disable ESP8266 Access point interface
access_point = network.WLAN(network.AP_IF)
access_point.active(False)


i2c = I2C(1, scl=Pin(15), sda=Pin(14))
bme = BME680_I2C(i2c=i2c)
led = Pin("LED", Pin.OUT)


def room_change(last_msg):
  """
  Changes room value if message contains sensor id
  :param last_msg last message from topic room_sub, must contain Sensor_id and room (example esp8266-67501400-test_room)
  """
  global room
  response_msg = None
  last_msg_list = tuple(last_msg.split("-"))
  if len(last_msg_list) == 3:
    msg_sensor_type, msg_sensor_id, msg_room = tuple(last_msg_list)
    print("Message {}".format(last_msg))
    print("From message sensor type is {} ID is {} and room is {}".format(
        msg_sensor_type, msg_sensor_id, msg_room))
    if msg_sensor_id in sensor_id and room != msg_room:
      room = msg_room
      response_msg = "UPDATE:Sensor [{}] changed room to [{}]".format(
          sensor_id, room)

  if response_msg:
    print(response_msg)
    client.publish(pub_sensor_status, response_msg)


def check_room(status_topic, sensor_id):
  client.publish(
      status_topic, "REQUEST:Sensor [{}] value [room].".format(sensor_id))
  time.sleep(2)
  client.check_msg()


def create_data_str(temp_arg, pres_arg, hum_arg, room_arg):
  """
  Creates data string in Influxdb data format.

  :param temp_arg Float with Temperature measured by BME680 Sensor
  :param pres_arg Float with Pressure measured by BME680 Sensor
  :param hum_arg Float with Humidity measured by BME680 Sensor
  :param room_arg String with Room in which sensor is located, removed from data if empty
  :return String in Influxdb format in order with all sensor values
  """
  if room_arg:
    MQTT_sensor_data = "sensor_data,sensor_id={0},board_type={1},sensor_type={2},room={3},comm_protocol=MQTT temperature={4:.2f},pressure={5:.2f},humidity={6:.2f}".format(
      sensor_id, board_type, sensor_type, room_arg, temp_arg, pres_arg, hum_arg)
  elif not room_arg:
    MQTT_sensor_data = "sensor_data,sensor_id={0},board_type={1},sensor_type={2},comm_protocol=MQTT temperature={3:.2f},pressure={4:.2f},humidity={5:.2f}".format(
      sensor_id, board_type, sensor_type, temp_arg, pres_arg, hum_arg)
  return MQTT_sensor_data


def read_bme_sensor():
  """
  Pulls data from BME680 sensor

  :return Tuple with measurements in order (Temp:Float, pres:Float, hum:Float)
  """
  # temp = ('{:.2f}'.format(bme.temperature))
  # pres = ('{:.2f}'.format(bme.pressure))
  # hum = ('{:.2f}'.format(bme.humidity))
  # gas = ('{:.3f}'.format(bme.gas))

  return bme.temperature, bme.pressure, bme.humidity
  # else:
  #  return('Invalid sensor readings.')


def publish_values(values_topic, data):
  print(data)
  client.publish(values_topic, data)


def sub_cb(topic, msg):
  if topic == sub_room:
    room_change(last_msg=msg.decode("utf-8"))


def connect_mqtt():
  client = MQTTClient(client_id, mqtt_server)
  # client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.set_callback(sub_cb)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  client.subscribe(sub_room)
  return client


def connect_to_wifi():
  # Connect to local network using Wi-fi
  mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
  print(f"\r\nSensor id: {sensor_id}")
  print(f"Device mac adress: {mac}")
  print(f"Connecting to {ssid}")
  station.connect(ssid, password)

  # Wait for connect or fail
  max_wait = 10
  while max_wait > 0:
    print(f"Connection status: {station.status()}")
    if station.status() < 0 or station.status() >= 3:
      break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(2)
  # Handle connection error
  if station.status() != 3:
    raise RuntimeError('Network connection failed')
  else:
    print(f'Connected to {ssid}')
    status = station.ifconfig()
    print('ip = ' + status[0])
    
    
    
def disconnect_from_wifi():
  station.disconnect()
  if station.isconnected() == False:
    print(f'Wifi connection {station.isconnected()} Succesfully disconnected')

def restart_and_reconnect():
  time.sleep(10)
  machine.soft_reset()

def put_to_light_sleep():
  print(f"Putting sensor in lightsleep mode for {message_interval_ms/1000} seconds in 5 seconds.")
  time.sleep(5)
  print(f"Sensor is now in lightsleep mode for {message_interval_ms/1000} seconds.")
  machine.lightsleep(message_interval_ms)

while True:
  try:
    led.toggle()
    time.sleep_ms(500)
    led.toggle()
    connect_to_wifi()
    client = connect_mqtt()
    client.check_msg()
    temp, pres, hum = read_bme_sensor()
    check_room(pub_sensor_status, sensor_id)
    publish_values(pub_values, create_data_str(temp, pres, hum, room))
    time.sleep(5)
    client.disconnect()
    disconnect_from_wifi()
    put_to_light_sleep()
  except OSError as e:
    print(f'Failed to read data from sensor. Attempting restart.')
    restart_and_reconnect()
  except RuntimeError as e:
    print(f'Failed to connect to MQTT broker on adress: {mqtt_server}. Attempting to restart and reconnect.')
    restart_and_reconnect()
  except:
    print(f'Unknown error. Attempting to reconnect.')
    restart_and_reconnect()

