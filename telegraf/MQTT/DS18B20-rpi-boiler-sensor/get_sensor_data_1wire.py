#!/usr/bin/env python3

import time
import paho.mqtt.client as mqtt
import subprocess

MQTT_SERVER = "192.168.88.107"
# Topics to publish
pub_values = 'sensor/values'
pub_sensor_status = 'sensor/status'

# Topics to subscribe
# sub_room = 'sensor/room'

def get_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line.split(":")[1].strip()

message_interval = 60
board_type = "raspi"
sensor_id = board_type + "-" + get_serial_number()
sensor_type = "1wire"
room = "water_boiler_room"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to {} MQTT broker  with result code {}".format(MQTT_SERVER, str(rc)))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe(sub_room)
 
# The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))
#     # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
# client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
client.loop_start()

while True:
     # vstupní teplota vody do radiátorů
    to_inp = float(subprocess.check_output(
        ['owread', '/28.9C873E1B1901/temperature']).decode().strip())
    # vstupní teplota vody do radiátorů
    to_out = float(subprocess.check_output(
        ['owread', '/28.41DA211C1901/temperature']).decode().strip())
    # vstupní teplota vody do radiátorů
    dhw_tmp = float(subprocess.check_output(
        ['owread', '/28.F6775F070000/temperature']).decode().strip())
    # vstupní teplota vody do radiátorů
    dhw_coil_temp = float(subprocess.check_output(
        ['owread', '/28.4618C1070000/temperature']).decode().strip())
    payload = "sensor_data,sensor_id={0},board_type={1},sensor_type={2},room={3},comm_protocol=MQTT tmp_in={4:.2f},tmp_out={5:.2f},dhw_tmp={6:.2f},dhw_coil_tmp={7:.2f}".format(
      sensor_id, board_type, sensor_type, room, to_inp, to_out, dhw_tmp, dhw_coil_temp)
    print(payload)

    client.publish(pub_values, str(payload))
    time.sleep(message_interval)