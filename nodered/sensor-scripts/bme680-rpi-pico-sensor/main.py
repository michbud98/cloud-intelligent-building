import utime
import ubinascii
import machine
from machine import Pin, I2C, RTC
from sys import print_exception
import micropython
import network, urequests, ujson
from bme680 import *

import gc

gc.collect()

ssid = 'SET WIFI NAME'
password = 'SET PASSWORD'
mqtt_server = 'SET NODERED SERVER IP'
# EXAMPLE IP ADDRESS
# nodered_server = '192.168.1.106'

# internal real time clock
rtc = RTC()
rtc_update_url = f"http://{nodered_server}:1880/datetime"  # rtc_update_url = "https://worldtimeapi.org/api/timezone/Europe/Prague"
nodered_influxdb_url = f"http://{nodered_server}:1880/postSensor"

client_id = ubinascii.hexlify(machine.unique_id())
board_type = "pico"
sensor_id = board_type + "-" + client_id.decode("utf-8")
sensor_type = "BME680"

# Message interval in milliseconds needs at least 10000 milliseconds
message_interval_ms = 60000

station = network.WLAN(network.STA_IF)
station.active(True)
# Disable ESP8266 Access point interface
access_point = network.WLAN(network.AP_IF)
access_point.active(False)

i2c = I2C(1, scl=Pin(27), sda=Pin(26))
bme = BME680_I2C(i2c=i2c)

led = Pin("LED", Pin.OUT)

# 0 ENABLED | 1 DISABLED
DEBUG_FILE = 1
DEBUG_LED = 1


def flash_led():
    if DEBUG_LED == 0:
        led.toggle()
        utime.sleep_ms(500)
        led.toggle()


def log(input_string, debug_file_override=1):
    # (year, month, day, weekday, hours, minutes, seconds, sub-seconds)
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
    print_exception(exception)
    print_exception(exception, file)
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
        utime.sleep(5)
        max_retry += 1

    if response and response.status_code == 200:
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
            response = urequests.post(nodered_influxdb_url, headers={'content-type': 'application/json'},
                                      data=json_data)
        except Exception as e:
            log_exception(e, "log.txt")
            log("Sending data to nodered failed. Retry after 5 sec")

        if response and response.status_code == 200:
            log(f"Sending data to Nodered successful.")
            break
        time.sleep(5)
        max_retry += 1


def connect_to_wifi():
    # Connect to local network using Wi-fi
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    log(f"Sensor id: {sensor_id}")
    log(f"Device mac address: {mac}")
    log(f"Connecting to {ssid}")
    station.connect(ssid, password)

    # Wait for connect or fail
    max_retry = 0
    while max_retry <= 15:
        log(f"Connection attempt {max_retry} status code: {station.status()}")
        if station.status() < 0 or station.status() >= 3:
            break
        max_retry += 1
        log("Waiting for connection...")
        utime.sleep(2)
    # Handle connection error
    if station.status() != 3:
        log(f"Status code {station.status()}. Sensor couldn't connect.")
        raise RuntimeError('Network connection failed')
    else:
        log(f"Status code {station.status()}. Connected to {ssid}")
        status = station.ifconfig()
        log(f"Sensor ip address = {status[0]}")


def disconnect_from_wifi():
    station.disconnect()
    if station.isconnected() == False:
        log(f"Wifi connection {station.isconnected()} Successfully disconnected")


def restart_and_reconnect():
    utime.sleep(10)
    log("Restarting sensor.")
    machine.soft_reset()


def put_to_light_sleep():
    log(f"Putting sensor in lightsleep mode for {message_interval_ms / 1000} seconds in 5 seconds.")
    utime.sleep(5)
    log(f"Sensor is now in lightsleep mode for {message_interval_ms / 1000} seconds.")
    machine.lightsleep(message_interval_ms)


while True:
    try:
        flash_led()
        connect_to_wifi()
        get_datetime_url(rtc_update_url)
        temp, pres, hum = read_bme_sensor()
        send_to_nodered(nodered_influxdb_url, temp, pres, hum)
        utime.sleep(5)
        disconnect_from_wifi()
        put_to_light_sleep()
    except OSError as e:
        log_exception(e, "log.txt")
        log(f"Failed to read data from sensor. Attempting restart.", 0)
        restart_and_reconnect()
    except RuntimeError as e:
        log_exception(e, "log.txt")
        log(f"Failed to connect to network on address: {nodered_server}. Attempting to restart and reconnect.", 0)
        restart_and_reconnect()
    except Exception as e:
        log_exception(e, "log.txt")
        log(f"Unknown exception {type(e).__name__}. Attempting to reconnect.", 0)
        restart_and_reconnect()