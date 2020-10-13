#!/usr/bin/env python3

import sys
import getopt
import time
import random

from subprocess import PIPE, Popen, check_output
import logging
import requests
from requests.exceptions import HTTPError, ConnectionError

import platform  # For getting the operating system name

# TODO Fix logging (after one cycle it wont write in file)
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

def check_connection_with_influxdb(url_domain: str):
    """
    Checks if influxdb is available on http address taken from param

    :param url_domain: url address of influxdb
    :return: Nothing
    :raises:
        HTTPError: exception is raised for invalid http responses (status code > 200)
        ConnectionError: ConnectionError exception is thrown in case of DNS failure,
        refused connection or any other connection related issues
    """
    # http example http://localhost:8086/ping
    logger.debug("Testing connection to {}".format(url_domain + str("ping")))
    response = requests.get(url_domain + str("ping"))
    logger.debug(f"Status code: {response.status_code}")
    # If the response was successful, no Exception will be raised
    response.raise_for_status()
    logger.info(f'Connection to {url_domain} successful')


def insert_into_influxdb(url_domain: str, database_name: str, data_string: str):
    """
    Runs insert operation in influxdb using curl command

    :param url_domain: url address of influxdb
    :param database_name: name of database to which we want to insert
    :param data_string: data which we want to insert in db
    :return: Nothing
    :raises:
        HTTPError: exception is raised for invalid http responses (status code > 200)
        ConnectionError: ConnectionError exception is thrown in case of DNS failure,
        refused connection or any other connection related issues
    """
    # http example 'http://localhost:8086/write?db=mydb'
    r = requests.post(url_domain + str(f"write?db={database_name}"), data=data_string)
    logger.debug("{} sent to {}".format(data_string, r.url))


def get_cpu_temperature() -> float:
    """
    Gets CPU temperature

    :return: Float CPU temperature value
    """
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


def print_help():
    logger.info("weather.py -d <debug> -s <sleep_time> -a <http_address>")


def main(argv):
    sleep_time: int = 60
    database_name_arg = "mydb"
    url_domain_arg: str = 'http://192.168.88.140:8086/'

    try:
        opts, args = getopt.getopt(argv, "hd:s:a:", ["help", "database=", "sleep=", "address=", "debug"])
    except getopt.GetoptError as argument_error:
        logger.error(argument_error.msg)
        print_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        if opt in ("-s", "--sleep"):
            sleep_time = int(arg)
        if opt in ("-d", "--database"):
            database_name_arg = arg
        if opt == "--debug":
            ch.setLevel(logging.DEBUG)
        if opt in ("-a", "--address"):
            url_domain_arg = arg

    logger.info("""weather.py - Print readings from the BME280 weather sensor.
       Press Ctrl+C to exit!
       """)

    while True:
        try:
            temperature = random.randint(-20, 40)
            pressure = random.randint(600, 900)
            humidity = random.randint(0, 100)
            logger.info("""
            Compensated_Temperature: {:05.2f} *C
            Pressure: {:05.2f} hPa
            Relative humidity: {:05.2f} %
            """.format(temperature, pressure, humidity))
            data_string = """
            temperature value={}
            pressure value={}
            humidity value={}""".format(temperature, pressure, humidity)
            check_connection_with_influxdb(url_domain_arg)
            insert_into_influxdb(url_domain_arg, database_name_arg, data_string)
            # TODO Add saving to local file
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
        except ConnectionError as conn_err:
            logger.error(f'Connection error occurred: {conn_err}')
        except Exception as err:
            logger.error(f'Other error occurred: {err}')
            sys.exit()

        logger.info(f"Sleeping for {sleep_time} second")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main(sys.argv[1:])
