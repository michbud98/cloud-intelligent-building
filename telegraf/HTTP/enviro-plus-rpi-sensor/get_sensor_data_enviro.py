#!/usr/bin/env python3

import sys
import time
import getopt

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from subprocess import PIPE, Popen, check_output

import platform  # For getting the operating system name
import subprocess  # For executing a shell command

import traceback


bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


def get_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line.split(":")[1].strip()


def get_cpu_temperature() -> float:
    """
    Gets CPU temperature

    :return: Float CPU temperature value
    """
    process = Popen(['vcgencmd', 'measure_temp'],
                    stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


def get_compensated_temperature() -> float:
    """
    Temporary method compensating heat from CPU

    :return: Float compensated temperature value
    """
    comp_factor = 2.25
    cpu_temp = get_cpu_temperature()
    raw_temp = bme280.get_temperature()
    comp_temp = raw_temp - ((cpu_temp - raw_temp) / comp_factor)
    # print("""
    # Compensated_Temperature: {:05.2f} *C
    # Pressure: {:05.2f} hPa
    # Relative humidity: {:05.2f} %
    # """.format(temperature, pressure, humidity))
    return comp_temp


def main():
    i = 0
    # First data from enviro sensor is flawed.
    # This gets data after 3 cycles each with 1 second waiting time
    while i <= 2:
        try:
            temperature = bme280.get_temperature()
            temperature_compensated = get_compensated_temperature()
            pressure = bme280.get_pressure()
            humidity = bme280.get_humidity()
            lux = ltr559.get_lux()
            prox = ltr559.get_proximity()
            i += 1
            time.sleep(1)
        except:
            print(traceback.format_exc())
    sensor_id = "raspi-" + get_serial_number()
    sensor_type = "Enviro-plus"
    # mymeasurement,tag1=tag1,tag2=tag2 fieldA="aaa",fieldB="bbb
    print("sensor_temperature,sensor_id={},sensor_type={} temperature={:.2f},temperature_compensated={:.2f}".format(
        sensor_id, sensor_type, temperature, temperature_compensated))
    print("sensor_pressure,sensor_id={},sensor_type={} pressure={:.2f}".format(sensor_id, sensor_type, pressure))
    print("sensor_humidity,sensor_id={},sensor_type={} humidity={:.2f}".format(sensor_id, sensor_type, humidity))
    print("sensor_light,sensor_id={},sensor_type={} light={:.2f},proximity={:.2f}".format(
        sensor_id, sensor_type, lux, prox))


if __name__ == "__main__":
    main()
