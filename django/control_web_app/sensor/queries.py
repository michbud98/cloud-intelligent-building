from django.shortcuts import get_object_or_404
from myutils.get_influx_data import query_field_val_from_db, \
    query_field_from_db, query_val_from_db, query_all_tag_values, get_bucket

from .models import Sensor
from room.models import Room

from typing import Dict, List, Tuple


def sort_sensor_ids(sensor_id_list: List[str]) -> Tuple[List[str], List[Sensor], List[Sensor]]:
    """
    Sorts sensor ids between two lists based on their availability in the django connected database. 
    If sensor is in the database it has set location.

    :param sensor_id_list: List of sensor_ids collected from Influxdb

    :return: Tuple with list of sensor ids without set location, list of objects Sensor 
    that contains sensor with set location (in database), list of objects Sensor with set location boiler
    """
    sensor_id_nonset = []
    sensor_id_set = []
    sensor_id_boiler = []
    for sensor_id in sensor_id_list:
        # Count = 1 -> one sensor with this sensor_id found in django db
        if Sensor.objects.filter(sensor_id=sensor_id).count() == 1:
            obj = Sensor.objects.get(sensor_id=sensor_id)
            if obj.location == "boiler":
                sensor_id_boiler.append(obj)
            else:
                sensor_id_set.append(obj)
        else:
            sensor_id_nonset.append(sensor_id)

    return sensor_id_nonset, sensor_id_set, sensor_id_boiler


def create_hostname_dict(sensor_id_list: List[str]) -> Dict[str, str]:
    """
    :param sensor_id_list: List of sensor_ids collected from Influxdb

    :return: Dictionary with sensor ids as keys and hostnames as values
    """
    sensor_id_hostnames: Dict[str] = {}
    for sensor_id in sensor_id_list:
        sensor_id_hostnames[sensor_id] = query_sensor_hostname(sensor_id)
    return sensor_id_hostnames

# REWORK I can add one querry with parameters and then I can call it from these methods
def query_sensor_hostname(sensor_id: str):
    hostname_query = "from(bucket: \"{}\")\
    |> range(start: -30d)\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> keyValues(keyColumns: [\"host\"])\
    |> keep(columns: [\"_value\"])\
    |> group()\
    |> distinct()".format(get_bucket(), sensor_id)
    return query_val_from_db(hostname_query)[0]

def create_sensor_type_dict(sensor_id_list: List[str]) -> Dict[str, str]:
    """
    :param sensor_id_list: List of sensor_ids collected from Influxdb

    :return: Dictionary with sensor ids as keys and sensor types as values
    """
    sensor_type_dict: Dict[str] = {}
    for sensor_id in sensor_id_list:
        sensor_type_dict[sensor_id] = query_sensor_type(sensor_id)
    return sensor_type_dict

def query_sensor_type(sensor_id: str):
    hostname_query = "from(bucket: \"{}\")\
    |> range(start: -30d)\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> keyValues(keyColumns: [\"sensor_type\"])\
    |> keep(columns: [\"_value\"])\
    |> group()\
    |> distinct()".format(get_bucket(), sensor_id)
    return query_val_from_db(hostname_query)[0]

def query_sensor_fields(sensor_id):
    fields_query = "from(bucket: \"{}\")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> keep(columns: [\"_field\"])\
    |> distinct()\
    |> keep(columns: [\"_field\"])\
    |> yield(name: \"mean\")".format(get_bucket(), sensor_id)
    return query_field_from_db(fields_query)

def query_last_sensor_temp(sensor_id):
    query = "from(bucket: \"{}\")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r._measurement == \"sensor_temperature\")\
        |> filter(fn: (r) => r._field == \"temperature\")\
        |> filter(fn: (r) => r.sensor_id == \"{}\")\
        |> last()".format(get_bucket(), sensor_id)
    result = query_field_val_from_db(query)
    if not result:
        return None
    else:
        return result[0][1]

def query_last_sensor_pressure(sensor_id):
    query = "from(bucket: \"{}\")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r._measurement == \"sensor_pressure\")\
        |> filter(fn: (r) => r._field == \"pressure\")\
        |> filter(fn: (r) => r.sensor_id == \"{}\")\
        |> last()".format(get_bucket(), sensor_id)
    result = query_field_val_from_db(query)
    if not result:
        return None
    else:
        return result[0][1]

def query_last_sensor_humidity(sensor_id):
    query = "from(bucket: \"{}\")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r._measurement == \"sensor_humidity\")\
        |> filter(fn: (r) => r._field == \"humidity\")\
        |> filter(fn: (r) => r.sensor_id == \"{}\")\
        |> last()".format(get_bucket(), sensor_id)
    result = query_field_val_from_db(query)
    if not result:
        return None
    else:
        return result[0][1]

def get_sensor_values(sensor_id):
    temp = query_last_sensor_temp(sensor_id)
    press = query_last_sensor_pressure(sensor_id)
    hum = query_last_sensor_humidity(sensor_id)
    return temp, press, hum
# ----------------------boiler-------------------------
def query_last_boiler_radiator_tmp_in(sensor_id):
    query = "from(bucket: \"{}\")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r._measurement == \"boiler_radiator_temp\")\
    |> filter(fn: (r) => r._field == \"tmp_in\")\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> last()".format(get_bucket(), sensor_id)
    result = query_field_val_from_db(query)
    if not result:
        return None
    else:
        return result[0][1]

def query_last_boiler_radiator_tmp_out(sensor_id):
    query = "from(bucket: \"{}\")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r._measurement == \"boiler_radiator_temp\")\
    |> filter(fn: (r) => r._field == \"tmp_out\")\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> last()".format(get_bucket(), sensor_id)
    result = query_field_val_from_db(query)
    if not result:
        return None
    else:
        return result[0][1]

def query_last_dwh_tmp(sensor_id):
    query = "from(bucket: \"{}\")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r._measurement == \"boiler_dhw\")\
    |> filter(fn: (r) => r._field == \"dhw_tmp\")\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> last()".format(get_bucket(), sensor_id)
    result = query_field_val_from_db(query)
    if not result:
        return None
    else:
        return result[0][1]

def query_last_dwh_coil_tmp(sensor_id):
    query = "from(bucket: \"{}\")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r._measurement == \"boiler_dhw\")\
    |> filter(fn: (r) => r._field == \"dhw_coil_temp\")\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> last()".format(get_bucket(), sensor_id)
    result = query_field_val_from_db(query)
    if not result:
        return None
    else:
        return result[0][1]

def get_boiler_values(sensor_id):
    tmp_in_get = query_last_boiler_radiator_tmp_in(sensor_id)
    tmp_out_get = query_last_boiler_radiator_tmp_out(sensor_id)
    dhw_tmp_get = query_last_dwh_tmp(sensor_id)
    dhw_coil_temp_get = query_last_dwh_coil_tmp(sensor_id)
    return tmp_in_get, tmp_out_get, dhw_tmp_get, dhw_coil_temp_get