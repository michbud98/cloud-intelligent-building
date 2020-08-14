#!/usr/bin/env python3

import sys
import getopt
import random
import time
import requests


def insert_into_influxdb(http: str, data_string: str):
    r = requests.post(http, data=data_string)
    print("{} sent to {}".format(data_string, r.url))

def print_help():
    print("influxdb_insert_test.py -s <sleep_time> -a <http_address>")

def main(argv):
    sleep_time: int = 60
    http: str = 'http://localhost:8086/write?db=mydb'

    try:
        # if there are no arguments raises exception
        if not argv:
            # print("No arguments")
            raise getopt.GetoptError("No arguments")
        opts, args = getopt.getopt(argv, "hs:a:", ["help", "sleep=", "address="])
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
        if opt in ("-a", "--address"):
            http = arg

    while True:
        temperature = random.randint(-20, 40)
        pressure = random.randint(-20, 40)
        humidity = random.randint(-20, 40)
        data_string = 'temperature value={} \n' \
                      'pressure value={} \n' \
                      'humidity value={}'.format(temperature, pressure, humidity)
        insert_into_influxdb(http, data_string)
        print(f"Sleeping for {sleep_time} second")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main(sys.argv[1:])
