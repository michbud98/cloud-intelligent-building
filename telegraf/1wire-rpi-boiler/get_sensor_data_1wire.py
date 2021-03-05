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

    sensor_id = "raspi-" + get_serial_number()
    sensor_type = "1wire"  # TODO Make dynamic
    print("boiler_radiator_temp,sensor_id={},sensor_type={} tmp_in={:.2f},tmp_out={:.2f}".format(
        sensor_id, sensor_type, to_inp, to_out))
    print("boiler_dhw,sensor_id={},sensor_type={} dhw_tmp={:.2f},dhw_coil_temp={:.2f}".format(
        sensor_id, sensor_type, dhw_tmp, dhw_coil_temp))


if __name__ == "__main__":
    main()

