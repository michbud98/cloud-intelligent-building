# Complete project details at https://RandomNerdTutorials.com/micropython-mqtt-publish-bme680-esp32-esp8266/

# ESP32 - Pin assignment
#i2c = I2C(scl=Pin(22), sda=Pin(21))
# ESP8266 - Pin assignment
i2c = I2C(scl=Pin(5), sda=Pin(4))
bme = BME680_I2C(i2c=i2c)

def log(input_string, debug_file_override = 1):
  log_text = f"{input_string}"
  if DEBUG_FILE == 0 or debug_file_override == 0:
    file = open("log.txt", "a")
    file.write(f"{log_text}\r\n")
    print(log_text)
    file.close()
  else:
    print(log_text)

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
    log("Message {}".format(last_msg))
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
  return MQTT_sensor_data

def read_bme_sensor():
  """
  Pulls data from BME680 sensor

  :return Tuple with measurements in order (Temp:Float, pres:Float, hum:Float)
  """
  try:
    # temp = ('{:.2f}'.format(bme.temperature))
    # pres = ('{:.2f}'.format(bme.pressure))
    # hum = ('{:.2f}'.format(bme.humidity))
    # gas = ('{:.3f}'.format(bme.gas))

    return bme.temperature, bme.pressure, bme.humidity
    #else:
    #  return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

def publish_values(values_topic, data):
  log(data)
  client.publish(values_topic, data)

def sub_cb(topic, msg):
  if topic == sub_room:
    room_change(last_msg = msg.decode("utf-8"))

def connect_mqtt():
  client = MQTTClient(client_id, mqtt_server)
  #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.set_callback(sub_cb)
  client.connect()
  log('Connected to %s MQTT broker' % (mqtt_server))
  client.subscribe(sub_room)
  return client

def connect_to_wifi():
  #Connect to local network using Wi-fi 
  station.active(True)
  mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
  log(f"\r\nSensor id: {sensor_id}")
  log(f"Device mac adress: {mac}")
  log(f"Connecting to {ssid}")
  station.connect(ssid, password)

  while station.isconnected() == False:
    pass

  if station.isconnected() == True:
    log('Connection to network successful')
    log(f'Network ip: {station.ifconfig()[0]}')

def disconnect_from_wifi():
  station.disconnect()
  if station.isconnected() == False:
    log(f'Wifi connection {station.isconnected()} Succesfully disconnected')

def restart_and_reconnect():
  log(f'Failed to connect to MQTT broker on adress: {mqtt_server}. Reconnecting...')
  time.sleep(10)
  machine.reset()

def put_to_deep_sleep():
  # check if the device woke from a deep sleep
  if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    log('Sensor woke from deep sleep')
  # set RTC.ALARM0 to fire after N seconds (waking the device)
  rtc.alarm(rtc.ALARM0, message_interval_ms)
  # put the device to sleep
  log(f"Putting sensor in deepsleep mode for {message_interval_ms/1000} seconds in 5 seconds.")
  time.sleep(5)
  log(f"Sensor is now in deepsleep mode for {message_interval_ms/1000} seconds.")
  machine.deepsleep()

while True:
  try:
    connect_to_wifi()
    client = connect_mqtt()
    client.check_msg()
    temp, pres, hum = read_bme_sensor()
    check_room(pub_sensor_status, sensor_id)
    publish_values(pub_values, create_data_str(temp, pres, hum, room))
    time.sleep(5)
    client.disconnect()
    disconnect_from_wifi()
    put_to_deep_sleep()
  except OSError as e:
    log(f'Failed to read data from sensor. Attempting restart.', 0)
    restart_and_reconnect()
  except Exception as e:
    file = open("log.txt", "a")
    sys.print_exception(e)
    sys.print_exception(e,file)
    file.close()
    log(f'Unknown exception {type(e).__name__}. Attempting to reconnect.', 0)
    restart_and_reconnect()
