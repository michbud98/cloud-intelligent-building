from sensor import queries as sensor_querries
from sensor.models import Sensor
from typing import Dict, List, Tuple

def create_temp_dict(sensor_set: List[Sensor]) -> Dict[str,str]:
    temp_dict = {}
    for sensor in sensor_set:
        temp_dict[sensor.sensor_id] = sensor_querries.query_last_sensor_temp(sensor.sensor_id)
    return temp_dict

def create_pressure_dict(sensor_set: List[Sensor]) -> Dict[str,str]:
    pressure_dict = {}
    for sensor in sensor_set:
        pressure_dict[sensor.sensor_id] = sensor_querries.query_last_sensor_pressure(sensor.sensor_id)
    return pressure_dict

def create_humidity_dict(sensor_set: List[Sensor]) -> Dict[str,str]:
    humidity_dict = {}
    for sensor in sensor_set:
        humidity_dict[sensor.sensor_id] = sensor_querries.query_last_sensor_humidity(sensor.sensor_id)
    return humidity_dict