#!/usr/bin/env python3

import sys
import getopt
import time

from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from subprocess import PIPE, Popen
import logging
import requests

# create logger with 'spam_application'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('weather_output.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                              "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


def insert_into_influxdb(http: str, data_string: str):
    r = requests.post(http, data=data_string)
    logger.debug("{} sent to {}".format(data_string, r.url))

def print_help():
    logger.info("weather.py -d <debug> -s <sleep_time> -a <http_address>")

def main(argv):
    sleep_time: int = 60
    http: str = 'http://192.168.88.140:8086/api/v2/write?bucket=mydb'

    logger.debug("Starting script with arguments \n"
                  "-s {} -a {}".format(sleep_time, http))

    try:
        opts, args = getopt.getopt(argv, "hds:a:", ["help", "debug", "sleep=", "address="])
    except getopt.GetoptError as argument_error:
        logger.warning(argument_error.msg)
        print_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        if opt in ("-s", "--sleep"):
            sleep_time = int(arg)
        if opt in ("-d", "--debug"):
            ch.setLevel(logging.DEBUG)
        if opt in ("-a", "--address"):
            http = arg

    logger.info("""weather.py - Print readings from the BME280 weather sensor.
       Press Ctrl+C to exit!
       """)

    while True:
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        logger.info("""
        Temperature: {:05.2f} *C
        Pressure: {:05.2f} hPa
        Relative humidity: {:05.2f} %
        """.format(temperature, pressure, humidity))
        data_string = 'temperature value={} \n' \
                      'pressure value={} \n' \
                      'humidity value={}'.format(temperature, pressure, humidity)
        insert_into_influxdb(http, data_string)
        time.sleep(sleep_time)


if __name__ == "__main__":
    main(sys.argv[1:])
