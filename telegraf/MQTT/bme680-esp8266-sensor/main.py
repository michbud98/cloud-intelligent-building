# Complete project details at https://RandomNerdTutorials.com/micropython-mqtt-publish-bme680-esp32-esp8266/

# ESP32 - Pin assignment
#i2c = I2C(scl=Pin(22), sda=Pin(21))
# ESP8266 - Pin assignment
i2c = I2C(scl=Pin(5), sda=Pin(4))

bme = BME680_I2C(i2c=i2c)

def room_change(last_msg):
  """
  Changes room value if message contains sensor id
  :param last_msg last message from topic room_sub, must contain Sensor_id and room (example esp8266-67501400-Michals_room)
  """
  global room
  last_msg_list = tuple(last_msg.split("-"))
  if len(last_msg_list) == 3:
    msg_sensor_type, msg_sensor_id, msg_room = tuple(last_msg_list)
    print("Message {}".format(last_msg))
    print("From message sensor type is {} ID is {} and room is {}".format(msg_sensor_type, msg_sensor_id, msg_room))
    if msg_sensor_id in sensor_id:
      room = msg_room
      client.publish(pub_sensor_status, "UPDATE:Sensor [{}] changed room to [{}]".format(sensor_id, room))
  else:
    client.publish(pub_sensor_status, 
    "Room change message [{}] has wrong format. Right format is (sensor_type-sensor_id-room).".format(last_msg))

def create_data_str(temp_arg, pres_arg, hum_arg, gas_arg, air_arg, room_arg):
  """
  Creates data string in Influxdb data format.

  :param temp_arg Float with Temperature measured by BME680 Sensor
  :param pres_arg Float with Pressure measured by BME680 Sensor
  :param hum_arg Float with Humidity measured by BME680 Sensor
  :param gas_arg Int with Gas measured by BME680 Sensor
  :param air_arg Float with Air quality calculated from humidity and gas measurement
  :param room_arg String with Room in which sensor is located, removed from data if empty
  :return String in Influxdb format in order with all sensor values
  """
  if room_arg:
    MQTT_sensor_data = "sensor_data,sensor_id={0},board_type={1},sensor_type={2},room={3},comm_protocol=MQTT temperature={4:.2f},pressure={5:.2f},humidity={6:.2f},gas={7},air_quality={8:.2f}".format(
      sensor_id, board_type, sensor_type, room_arg, temp_arg, pres_arg, hum_arg, gas_arg, air_arg)
  elif not room_arg:
    MQTT_sensor_data = "sensor_data,sensor_id={0},board_type={1},sensor_type={2},comm_protocol=MQTT temperature={3:.2f},pressure={4:.2f},humidity={5:.2f},gas={6:.2f},air_quality={7:.2f}".format(
      sensor_id, board_type, sensor_type, temp_arg, pres_arg, hum_arg, gas_arg, air_arg)
  return MQTT_sensor_data

def sub_cb(topic, msg):
  if topic == sub_room:
    room_change(last_msg = msg.decode("utf-8"))

def connect_mqtt():
  client = MQTTClient(client_id, mqtt_server)
  #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.set_callback(sub_cb)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  client.subscribe(sub_room)
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def get_gas_baseline(start_time, burn_in_time):
  """
  Collect gas resistance burn-in values, then use the average of the last 50 values to set the upper limit 
  for calculatin gas_baseline. Needs to run at least for 5 min (300 sec) or more.

  :return Gas baseline for measuring air quality
  """
  burn_in_data = []
  led.value(0)
  print("Collecting gas resistance burn-in data for {} min\n".format(burn_in_time/60))
  while time.time() - start_time < burn_in_time:
    print (time.time() - start_time)
    gas = read_gas_bme_sensor()
    if isinstance(gas, int) or isinstance(gas, float):
      burn_in_data.append(gas)
      print('Gas: {0} Ohms'.format(gas)) 
      if (time.time() - start_time) % 30 == 0:
        time_remaining = (burn_in_time - (time.time() - start_time))/60
        print("Sensor {} calibrating. Time remaining {} min".format(sensor_id, time_remaining))
        client.publish(pub_sensor_status, "Sensor {} calibrating. Time remaining {} min".format(sensor_id, time_remaining))
    time.sleep(1)

  led.value(1)
  gas_baseline = sum(burn_in_data[-50:]) / 50.0
  return gas_baseline

def get_air_quality(hum, gas):
  """
  Measures air quality based on gas resistence value and humidity value from BME680 sensor.

  :return Float air quality in percent
  """
  gas_offset = gas_baseline - gas
  hum_offset = hum - hum_baseline
  # Calculate hum_score as the distance from the hum_baseline.
  if hum_offset > 0:
      hum_score = (100 - hum_baseline - hum_offset)
      hum_score /= (100 - hum_baseline)
      hum_score *= (hum_weighting * 100)

  else:
      hum_score = (hum_baseline + hum_offset)
      hum_score /= hum_baseline
      hum_score *= (hum_weighting * 100)

  # Calculate gas_score as the distance from the gas_baseline.
  if gas_offset > 0:
      gas_score = (gas / gas_baseline)
      gas_score *= (100 - (hum_weighting * 100))

  else:
      gas_score = 100 - (hum_weighting * 100)

  # Calculate air_quality_score.
  return hum_score + gas_score

def read_gas_bme_sensor():
  """
  Pulls data from BME680 sensor

  :return Int gas value measured by sensor
  """
  try:
    gas = bme.gas
    return gas
    #else:
    #  return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

def read_bme_sensor():
  """
  Pulls data from BME680 sensor

  :return Tuple with measurements in order (Temp:Float, pres:Float, hum:Float, gas:Int)
  """
  try:
    # temp = ('{:.2f}'.format(bme.temperature))
    # pres = ('{:.2f}'.format(bme.pressure))
    # hum = ('{:.2f}'.format(bme.humidity))
    # gas = ('{:.3f}'.format(bme.gas))

    return bme.temperature, bme.pressure, bme.humidity, bme.gas
    #else:
    #  return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

gas_baseline = get_gas_baseline(time.time(), burn_time)
#gas_baseline = 300000
# Set the humidity baseline to 40%, an optimal indoor humidity.
hum_baseline = 40.0
# This sets the balance between humidity and gas reading in the
# calculation of air_quality_score (25:75, humidity:gas)
hum_weighting = 0.25

print("Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n".format(gas_baseline,hum_baseline))
client.publish(pub_sensor_status, "Sensor calibrated. Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n".format(gas_baseline,hum_baseline))

while True:
  try:
    client.check_msg()
    temp, pres, hum, gas = read_bme_sensor()
    if (time.time() - last_message) > message_interval:
      if not room:
        print("Room value is empty, requesting room.\r\nREQUEST:Sensor [{}] value [room].".format(sensor_id))
        client.publish(pub_sensor_status, "REQUEST:Sensor [{}] value [room].".format(sensor_id))
        time.sleep(5)
        client.check_msg()
      print("Sensor {} measured Gas: {} kOhms\r\n".format(sensor_id, gas))
      air_quality = get_air_quality(hum,gas)
      #print("Air quality score {} %".format(air_quality))
      MQTT_sensor_data = create_data_str(temp, pres, hum, gas, air_quality, room)
      print(MQTT_sensor_data)
      client.publish(pub_values, MQTT_sensor_data)
      
      last_message = time.time()
    time.sleep(1)
  except OSError as e:
    restart_and_reconnect()
