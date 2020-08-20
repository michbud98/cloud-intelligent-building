#!/usr/bin/env python3

import sys
import getopt
import random
import time
import requests
from requests.exceptions import HTTPError, ConnectionError
from subprocess import PIPE, Popen, check_output


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
    print("Testing connection to {}".format(url_domain + str("ping")))
    response = requests.get(url_domain + str("ping"))
    print(f"Status code: {response.status_code}")
    # If the response was successful, no Exception will be raised
    response.raise_for_status()
    print('Connection successful')


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
    print("{} sent to {}".format(data_string, r.url))


# Check for Wi-Fi connection (takhle metoda na Macu nefunguje na raspberry ano)
def check_wifi():
    if check_output(['hostname', '-I']):
        return True
    else:
        return False


def print_help():
    print("influxdb_insert_test.py -s <sleep_time> -a <http_address>")


def main(argv):
    sleep_time: int = 60
    database_name_arg = "nodb"
    url_domain_arg: str = 'http://localhost:8086/'

    try:
        opts, args = getopt.getopt(argv, "hd:s:a:", ["help", "database=", "sleep=", "address=", "debug"])
    except getopt.GetoptError as argument_error:
        print(argument_error.msg)
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
        if opt in "--debug":
            print("Setting log on debug")
        if opt in ("-a", "--address"):
            url_domain_arg = arg

    while True:
        try:
            temperature = random.randint(-20, 40)
            pressure = random.randint(-20, 40)
            humidity = random.randint(-20, 40)
            data_string = 'temperature value={} \n' \
                          'pressure value={} \n' \
                          'humidity value={}'.format(temperature, pressure, humidity)
            check_connection_with_influxdb(url_domain_arg)
            insert_into_influxdb(url_domain_arg, database_name_arg, data_string)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
            sys.exit()

        print(f"Sleeping for {sleep_time} second")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main(sys.argv[1:])
