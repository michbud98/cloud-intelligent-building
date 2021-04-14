from django.shortcuts import get_object_or_404
from myutils.get_influx_data import query_field_val_from_db, \
    query_field_from_db, query_val_from_db, query_all_tag_values, get_bucket

from sensor import queries as sensor_querries

from sensor.models import Sensor

from typing import Dict, List, Tuple

def query_avg_values_from_location(location):
    sensor_set = Sensor.objects.filter(location=location)
    tmp_list, pres_list, hum_list = [], [], []
    
    for sensor in sensor_set:
        temperature, pressure, humidity = get_sensor_values(sensor.sensor_id)
        if temperature != None and pressure != None and humidity != None:
            tmp_list.append(temperature)
            pres_list.append(pressure)
            hum_list.append(humidity)

    return round(get_list_average(tmp_list),2), round(get_list_average(pres_list),2), round(get_list_average(hum_list),2), 

def get_sensor_values(sensor_id):
    temp = sensor_querries.query_last_sensor_temp(sensor_id)
    pres = sensor_querries.query_last_sensor_pressure(sensor_id)
    hum = sensor_querries.query_last_sensor_humidity(sensor_id)
    
    return temp, pres, hum

def get_list_average(lst): 
    if len(lst) == 0:
        return 0
    else:
        return sum(lst) / len(lst) 

def get_boiler_values():
    sensor_set = Sensor.objects.filter(location="boiler")
    tmp_in, tmp_out, dwh_tmp, dwh_coil_tmp = [], [], [], []

    # REWORK This will always return last boiler
    for sensor in sensor_set:
        tmp_in, tmp_out, dwh_tmp, dwh_coil_tmp = sensor_querries.get_boiler_values(sensor.sensor_id)

    return tmp_in, tmp_out, dwh_tmp, dwh_coil_tmp

    
        