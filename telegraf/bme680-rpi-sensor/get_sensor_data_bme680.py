#!/usr/bin/env python
import bme680


try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)


# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_2X)
sensor.set_temperature_oversample(bme680.OS_2X)
sensor.set_filter(bme680.FILTER_SIZE_1)


def get_serial_number():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line.split(":")[1].strip()


def main():
    if sensor.get_sensor_data():
        temperature = sensor.data.temperature
        pressure = sensor.data.pressure
        humidity = sensor.data.humidity

        sensor_id = "raspi-" + get_serial_number()
        sensor_type = "BME680" # TODO Make dynamic
        print("sensor_temperature,sensor_id={},sensor_type={} temperature={:.2f}".format(
            sensor_id, sensor_type,temperature))
        print("sensor_pressure,sensor_id={},sensor_type={} pressure={:.2f}".format(sensor_id, sensor_type, pressure))
        print("sensor_humidity,sensor_id={},sensor_type={} humidity={:.2f}".format(sensor_id, sensor_type, humidity))

if __name__ == "__main__":
    main()
