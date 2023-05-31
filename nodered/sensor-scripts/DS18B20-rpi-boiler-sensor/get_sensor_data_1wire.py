#!/usr/bin/env python3

import subprocess, requests, time, json
import gc

def get_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line.split(":")[1].strip()

board_type = "raspi"
sensor_id = board_type + "-" + get_serial_number()
sensor_type = "1wire"
room_arg = "water_boiler_room"

nodered_server = '192.168.88.107'
nodered_influxdb_url = f"http://{nodered_server}:1880/postBoiler"

message_interval = 60

def send_to_nodered(nodered_influxdb_url, tmp_in, tmp_out, dhw_tmp, dhw_coil_tmp):
    response = None
    data = {
        "sensor_id": sensor_id,
        "board_type": board_type,
        "sensor_type": sensor_type,
        "tmp_in": tmp_in,
        "tmp_out": tmp_out,
        "dhw_tmp": dhw_tmp,
        "dhw_coil_tmp": dhw_coil_tmp
    }
    json_data = json.dumps(data);
    print(f"Encoded json data: {json_data}");

    max_retry = 0
    while max_retry <= 10:
        try:
            print(f"Sending sensor data to Nodered on {nodered_influxdb_url}. Try number {max_retry}")
            response = requests.post(nodered_influxdb_url, headers={'content-type': 'application/json'},
                                      data=json_data)
        except Exception as e:
            print(e)
            print("Sending data to nodered failed. Retry after 5 sec")

        if response is not None and response.status_code >= 200 and response.status_code < 300:
            print(f"Sending data to Nodered successful.")
            response.close()
            gc.collect()
            break

        elif response is not None and response.status_code >= 400 and response.status_code < 500:
            print(f"Error status code {response.status_code}: {response.text} \r\nRestarting sensor");
            response.close()
            gc.collect()
            break

        time.sleep(5)
        max_retry += 1


def main():
    while True:
        # vstupní teplota vody do radiátorů
        tmp_in = float(subprocess.check_output(
            ['owread', '/28.9C873E1B1901/temperature']).decode().strip())
        # vstupní teplota vody do radiátorů
        tmp_out = float(subprocess.check_output(
            ['owread', '/28.41DA211C1901/temperature']).decode().strip())
        # vstupní teplota vody do radiátorů
        dhw_tmp = float(subprocess.check_output(
            ['owread', '/28.F6775F070000/temperature']).decode().strip())
        # vstupní teplota vody do radiátorů
        dhw_coil_tmp = float(subprocess.check_output(
            ['owread', '/28.4618C1070000/temperature']).decode().strip())


        send_to_nodered(nodered_influxdb_url, tmp_in, tmp_out, dhw_tmp,dhw_coil_tmp)

        print(f"Putting sensor to sleep for {message_interval}.")
        time.sleep(message_interval)

if __name__ == "__main__":
    main()

