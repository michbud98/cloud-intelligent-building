#!/usr/bin/env python3

import subprocess


def get_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line.split(":")[1].strip()


def main():
    # vstupní teplota vody do radiátorů
    to_inp = float(subprocess.check_output(
        ['owread', '/28.9C873E1B1901/temperature']).decode().strip())
    # vstupní teplota vody do radiátorů
    to_out = float(subprocess.check_output(
        ['owread', '/28.41DA211C1901/temperature']).decode().strip())
    # vstupní teplota vody do radiátorů
    dhw_tmp = float(subprocess.check_output(
        ['owread', '/28.F6775F070000/temperature']).decode().strip())
    # vstupní teplota vody do radiátorů
    dhw_coil_temp = float(subprocess.check_output(
        ['owread', '/28.4618C1070000/temperature']).decode().strip())

    board_type = "raspi"
    sensor_id = board_type + "-" + get_serial_number()
    sensor_type = "1wire"
    room_arg = "water_boiler_room"
    print("sensor_data,sensor_id={0},board_type={1},sensor_type={2},room={3},comm_protocol=HTTP tmp_in={4:.2f},tmp_out={5:.2f},dhw_tmp={6:.2f},dhw_coil_tmp={7:.2f}".format(
      sensor_id, board_type, sensor_type, room_arg, to_inp, to_out, dhw_tmp, dhw_coil_temp))


if __name__ == "__main__":
    main()

