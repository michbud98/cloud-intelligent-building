#!/usr/bin/env python3

import sys
import argparse
import re
import requests
from bs4 import BeautifulSoup


def get_sensor_data_html(sensor_url: str) -> str:
    """
    Gets html from nodemcu sensor
    :param sensor_url: url to sensor
    :return:  String with html
    """
    html = requests.get(sensor_url)
    return html


def get_sensor_id(html: str):
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all('small')
    for result in results:
        x = re.sub(" ", "|", result.text)
        return x.split("|")[1]


def get_sensor_measurement(html: str, regex: str) -> int:
    """
    Separates value set by regex using BeautifulSoup
    :param html: html from sensor
    :param regex: Regular expression specifying value we want (recommend finding unit of value)
    :return:  Tuple(sensor_type,measured_value)
    """
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all('tr')
    for result in results:
        values = result.find_all('td')
        if(not values or not values[0].text.strip() or values[0].text.strip() == "WiFi"):
            # If line is empty, contains only whitespace or Sensor type value is WiFi,skips line
            continue
        matcher = re.search(regex, values[2].text.strip())  # example "°[cC]$"
        if(matcher):
            sensor_type = values[0].text.strip()
            sensor_value = get_value(values[2].text.strip(), regex)

    return sensor_type, sensor_value


def get_value(value_str: str, regex: str) -> float:
    """
    Changes value from string to float
    :param value_str: value in string
    :param regex: Regular expression specifying unit of value we need to remove from string
    :return:  value in float
    """
    # r.sub finds characters specified by regex and replaces them with empty string
    value = float(re.sub(regex, "", value_str))
    return value


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action="store", dest="url",
                        help="URL of luftdaten sensor")
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    if args.url is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # "http://192.168.77.108/values"
    sensor_html = get_sensor_data_html(args.url)
    board_type = "luftdaten"
    sensor_id = board_type + "-" + get_sensor_id(sensor_html)
    temp_arg = get_sensor_measurement(sensor_html, "°[cC]$")[1]
    pres_arg = get_sensor_measurement(sensor_html, "hPa")[1]
    hum_arg = get_sensor_measurement(sensor_html, "%$")[1]
    sensor_type = get_sensor_measurement(sensor_html, "°[cC]$")[0]

    print("sensor_data,sensor_id={0},board_type={1},sensor_type={2},room=Outdoors,comm_protocol=Scrap temperature={3},pressure={4},humidity={5}".format(
      sensor_id, board_type, sensor_type, temp_arg, pres_arg, hum_arg))

if __name__ == "__main__":
    main()
