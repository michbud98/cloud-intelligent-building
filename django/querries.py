# REWORK I think this is not the best implementation, but it will do for now

from get_influx_data import query_data_from_influxdb

def last_indoors_temperature():
    temperature_indoors_query = 'from(bucket: "Sensor_data")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r["_measurement"] == "sensor_temperature")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> filter(fn: (r) => r["host"] == "raspberrypi")\
    |> last()'
    return query_data_from_influxdb(temperature_indoors_query)[0][1]

# print("Last indoors temperature {}".format(last_indoors_temperature()))

def last_outdoors_temperature():
    temperature_outdoors_query= 'from(bucket: "Sensor_data")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r["_measurement"] == "sensor_temperature")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> filter(fn: (r) => r["host"] == "telegraf-docker")\
    |> last()'
    return query_data_from_influxdb(temperature_outdoors_query)[0][1]

# print("Last outdoors temperature {}".format(last_outdoors_temperature()))

def last_indoors_pressure():
    pressure_indoors_query = 'from(bucket: "Sensor_data")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r["_measurement"] == "sensor_pressure")\
        |> filter(fn: (r) => r["_field"] == "pressure")\
        |> filter(fn: (r) => r["host"] == "raspberrypi")\
        |> last()'
    return query_data_from_influxdb(pressure_indoors_query)[0][1]

# print("Last indoors pressure {}".format(last_indoors_pressure()))

def last_outdoors_pressure():
    pressure_outdoors_querry = 'from(bucket: "Sensor_data")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r["_measurement"] == "sensor_pressure")\
        |> filter(fn: (r) => r["_field"] == "pressure")\
        |> filter(fn: (r) => r["host"] == "telegraf-docker")\
        |> last()'
    return query_data_from_influxdb(pressure_outdoors_querry)[0][1]

print("Last outdoors pressure {}".format(last_outdoors_pressure()))

def last_indoors_humidity():
    humidity_indoors_querry = 'from(bucket: "Sensor_data")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r["_measurement"] == "sensor_humidity")\
        |> filter(fn: (r) => r["_field"] == "humidity")\
        |> filter(fn: (r) => r["host"] == "raspberrypi")\
        |> last()'
    return query_data_from_influxdb(humidity_indoors_querry)[0][1]

# print("Last indoors humidity {}".format(last_indoors_humidity()))

def last_outdoors_humidity():
    humidity_outdoors_querry = 'from(bucket: "Sensor_data")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r["_measurement"] == "sensor_humidity")\
        |> filter(fn: (r) => r["_field"] == "humidity")\
        |> filter(fn: (r) => r["host"] == "telegraf-docker")\
        |> last()'
    return query_data_from_influxdb(humidity_outdoors_querry)[0][1]

print("Last outdoors humidity {}".format(last_outdoors_humidity()))

def last_indoors_light():
    light_indoors_query= 'from(bucket: "Sensor_data")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r["_measurement"] == "sensor_light")\
        |> filter(fn: (r) => r["_field"] == "light")\
        |> filter(fn: (r) => r["host"] == "raspberrypi")\
        |> last()'
    return query_data_from_influxdb(light_indoors_query)[0][1]

# print("Last indoors light {}".format(last_indoors_light()))