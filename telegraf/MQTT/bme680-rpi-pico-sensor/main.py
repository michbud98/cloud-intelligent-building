import time
from umqttsimple import MQTTClient
import ubinascii
import machine
from machine import Pin, I2C
from sys import print_exception
import micropython
import network
from bme680 import *
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

DEBUG_FILE = 1
DEBUG_LED = 1

def flash_led():
  if DEBUG_LED == 0:
    led.toggle()
    time.sleep_ms(500)
    led.toggle()

def log(input_string, debug_file_override = 1):
  log_text = f"{input_string}"
  if DEBUG_FILE == 0 or debug_file_override == 0:
    file = open("log.txt", "a")
    file.write(f"{log_text}\r\n")
    print(log_text)
    file.close()
  else:
    print(log_text)

def log_exception(exception, file_name):
  file = open(file_name, "a")
  print_exception(exception)
  print_exception(exception,file)
  file.close()


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
    log("Recieved message {}".format(last_msg))
    log("From message sensor type is {} ID is {} and room is {}".format(msg_sensor_type, msg_sensor_id, msg_room))
    if msg_sensor_id in sensor_id and room != msg_room:
      room = msg_room
      response_msg = "UPDATE:Sensor [{}] changed room to [{}]".format(sensor_id, room)
  if response_msg:
    log(response_msg)
    client.publish(pub_sensor_status, response_msg)


def check_room(status_topic, sensor_id):
  log("Sending room value request to database.")
  client.publish(status_topic, "REQUEST:Sensor [{}] value [room].".format(sensor_id))
  max_wait = 0
  while not room and max_wait <= 10:
    log(f"Checking for response. Attempt {max_wait}")
    time.sleep(1)
    client.check_msg()
    max_wait += 1


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
  log(f"Created Influx data: {MQTT_sensor_data}")
  return MQTT_sensor_data


def read_bme_sensor():
  """
  Pulls data from BME680 sensor

  :return Tuple with measurements in order (Temp:Float, pres:Float, hum:Float)
  """
  temp = bme.temperature
  pres = bme.pressure
  hum = bme.humidity
  #gas = ('{:.3f}'.format(bme.gas))
  log(f"Pulled data from BME680 sensor:\r\nTemperature: {temp}\r\nPressure: {pres}\r\nHumidity: {hum}")
  return temp, pres, hum
  # else:
  #  return('Invalid sensor readings.')


def publish_values(values_topic, data):
  log(f"Published values {data}")
  client.publish(values_topic, data)


def sub_cb(topic, msg):
  if topic == sub_room:
    room_change(last_msg=msg.decode("utf-8"))


def connect_mqtt():
  client = MQTTClient(client_id, mqtt_server)
  # client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.set_callback(sub_cb)
  client.connect()
  log(f"Connected to {mqtt_server} MQTT broker")
  client.subscribe(sub_room)
  return client


def connect_to_wifi():
  # Connect to local network using Wi-fi
  mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
  log(f"Sensor id: {sensor_id}")
  log(f"Device mac adress: {mac}")
  log(f"Connecting to {ssid}")
  station.connect(ssid, password)

  # Wait for connect or fail
  max_wait = 0
  while max_wait <= 15:
    log(f"Connection attempt {max_wait} status code: {station.status()}")
    if station.status() < 0 or station.status() >= 3:
      break
    max_wait += 1
    log("Waiting for connection...")
    time.sleep(2)
  # Handle connection error
  if station.status() != 3:
    log(f"Status code {station.status()}. Sensor couldn't connect.")
    raise RuntimeError('Network connection failed')
  else:
    log(f"Status code {station.status()}. Connected to {ssid}")
    status = station.ifconfig()
    log(f"Sensor ip adress = {status[0]}")
    
    
    
def disconnect_from_wifi():
  station.disconnect()
  if station.isconnected() == False:
    log(f"Wifi connection {station.isconnected()} Succesfully disconnected")

def restart_and_reconnect():
  time.sleep(10)
  log("Restarting sensor.")
  machine.soft_reset()

def put_to_light_sleep():
  log(f"Putting sensor in lightsleep mode for {message_interval_ms/1000} seconds in 5 seconds.")
  time.sleep(5)
  log(f"Sensor is now in lightsleep mode for {message_interval_ms/1000} seconds.")
  machine.lightsleep(message_interval_ms)

while True:
  try:
    flash_led()
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
    log_exception(e, "log.txt")
    log(f"Failed to read data from sensor. Attempting restart.", 0)
    restart_and_reconnect()
  except RuntimeError as e:
    log_exception(e, "log.txt")
    log(f"Failed to connect to MQTT broker on adress: {mqtt_server}. Attempting to restart and reconnect.", 0)
    restart_and_reconnect()
  except Exception as e:
    log_exception(e, "log.txt")
    log(f"Unknown exception {type(e).__name__}. Attempting to reconnect.", 0)
    restart_and_reconnect()
