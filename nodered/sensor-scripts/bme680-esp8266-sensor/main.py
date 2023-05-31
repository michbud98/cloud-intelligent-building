# ESP32 - Pin assignment
# i2c = I2C(scl=Pin(22), sda=Pin(21))
# ESP8266 - Pin assignment
i2c = I2C(scl=Pin(5), sda=Pin(4))
bme = BME680_I2C(i2c=i2c)


def log(input_string, debug_file_override=1):
    # (year, month, day, weekday, hours, minutes, seconds, subseconds)
    datetime = rtc.datetime()
    datetime_str = f"{datetime[2]}.{datetime[1]}.{datetime[0]}|-|{datetime[4]}-{datetime[5]}-{datetime[6]}"
    log_text = f"{datetime_str}: {input_string}"
    if DEBUG_FILE == 0 or debug_file_override == 0:
        file = open("log.txt", "a")
        file.write(f"{log_text}\r\n")
        print(log_text)
        file.close()
    else:
        print(log_text)


def log_exception(exception, file_name):
    file = open(file_name, "a")
    sys.print_exception(exception)
    sys.print_exception(exception, file)
    file.close()

def get_datetime_url(datetime_url):
    response = None
    max_retry = 0
    while max_retry <= 10:
        try:
            log(f"Requesting datetime from {datetime_url}. Try number {max_retry}")
            response = urequests.get(datetime_url)
        except:
            log("Datetime request failed. Retry after 5 sec")
        if response and response.status_code == 200:
            log(f"Datetime request successful.")
            break
        time.sleep(5)
        max_retry += 1

    if response is not None and response.status_code >= 200 and response.status_code < 300:
        log(response.text)
        parsed = response.json()
        datetime_str = str(parsed["datetime"])
        year = int(datetime_str[0:4])
        month = int(datetime_str[5:7])
        day = int(datetime_str[8:10])
        hour = int(datetime_str[11:13])
        minute = int(datetime_str[14:16])
        second = int(datetime_str[17:19])

        # update internal RTC
        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
        log(f"RTC updated. Current datetime is: {rtc.datetime()}")

        response.close();
        gc.collect();
    else:
        log("RTC update failed")


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
    # gas = ('{:.3f}'.format(bme.gas))
    log(f"Pulled data from BME680 sensor:\r\nTemperature: {temp}\r\nPressure: {pres}\r\nHumidity: {hum}")
    return temp, pres, hum
    # else:
    #  return('Invalid sensor readings.')

def send_to_nodered(nodered_influxdb_url, temp_arg, pres_arg, hum_arg):
    response = None
    data = {
        "sensor_id": sensor_id,
        "board_type": board_type,
        "sensor_type": sensor_type,
        "temperature": temp_arg,
        "pressure": pres_arg,
        "humidity": hum_arg
    }
    json_data = ujson.dumps(data);
    log(f"Encoded json data: {json_data}");

    max_retry = 0
    while max_retry <= 10:
        try:
            log(f"Sending sensor data to Nodered on {nodered_influxdb_url}. Try number {max_retry}")
            response = urequests.post(nodered_influxdb_url, headers = {'content-type': 'application/json'}, data = json_data)
        except Exception as e:
            log_exception(e, "log.txt")
            log("Sending data to nodered failed. Retry after 5 sec")


        if response is not None and response.status_code >= 200 and response.status_code < 300:
            log(f"Sending data to Nodered successful.")
            response.close();
            gc.collect();
            break

        elif response is not None and response.status_code >= 400 and response.status_code < 500:
            log(f"Error status code {response.status_code}: {response.text} \r\nRestarting sensor.", 0);
            response.close()
            gc.collect()
            break


        time.sleep(5)
        max_retry += 1

def connect_to_wifi():
    # Connect to local network using Wi-fi
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
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
        log(f'Wifi connection {station.isconnected()} Successfully disconnected')


def restart_and_reconnect():
    log(f'Failed to connect to Nodered on address: {nodered_server}. Reconnecting...')
    time.sleep(10)
    machine.reset()


def put_to_deep_sleep():
    # check if the device woke from a deep sleep
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        log('Sensor woke from deep-sleep')
    # set RTC.ALARM0 to fire after N seconds (waking the device)
    rtc.alarm(rtc.ALARM0, message_interval_ms)
    # put the device to sleep
    log(f"Putting sensor in deep-sleep mode for {message_interval_ms / 1000} seconds in 5 seconds.")
    time.sleep(5)
    log(f"Sensor is now in deep-sleep mode for {message_interval_ms / 1000} seconds.")
    machine.deepsleep()


while True:
    try:
        connect_to_wifi()
        get_datetime_url(rtc_update_url)
        temp, pres, hum = read_bme_sensor()
        send_to_nodered(nodered_influxdb_url, temp, pres, hum)
        disconnect_from_wifi()
        put_to_deep_sleep()
    except OSError as e:
        log_exception(e, "log.txt")
        log(f'Failed to read data from sensor. Attempting restart.', 0)
        restart_and_reconnect()
    except Exception as e:
        log_exception(e, "log.txt")
        log(f'Unknown exception {type(e).__name__}. Attempting to reconnect.', 0)
        restart_and_reconnect()

