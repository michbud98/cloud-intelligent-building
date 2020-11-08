#!/usr/bin/env python3

import sys
import time
import getopt

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

def get_cpu_temperature() -> float:
    """
    Gets CPU temperature

    :return: Float CPU temperature value
    """
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
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



def main(argv):
    try:
        # TODO find out which temperature collection is more accurate raw/compensated
        #temperature = bme280.get_temperature()
        temperature = get_compensated_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        print("sensor_temperature temperature={}".format(temperature))
        print("sensor_pressure pressure={}".format(pressure))
        print("sensor_humidity humidity={}".format(humidity))
    except:
        print(traceback.format_exc())
        

if __name__ == "__main__":
    main(sys.argv[1:])


