import os
from pathlib import Path

import influxdb_client
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
bucket = "Sensor_data"
org = "swiftblade1982@gmail.com"
# Gets Influx token from file
# with open(os.path.join(BASE_DIR, "secrets/influx_cloud_token.txt")) as f:
#     token = f.read().strip()

token = os.getenv("INFLUX_TOKEN", None)
if(token is None):
    raise RuntimeError("Environment variable INFLUX_TOKEN not found.")
# Store the URL of your InfluxDB instance
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

def get_bucket():
    return bucket

def query_field_val_from_db(query: str) -> List[tuple]:
    """
    Queries Measurement field and value from InfluxDB database

    :param query: Query which specifies data we want to get from InfluxDB (uses Flux)
    
    :return: List of tuples (Measurement field name, Measurement value)
    """
    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results

def query_field_from_db(query: str) -> List[str]:
    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(record.get_field())
    return results

def query_val_from_db(query: str) -> List[str]:
    """
    Queries Measurement value from InfluxDB database

    :param query: Query which specifies data we want to get from InfluxDB (uses Flux)

    :return: List of tuples (Measurement value)
    """
    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(record.get_value())
    return results

def query_all_tag_values(tag) -> List[str]:
    """
    Queries all values of selected tag

    :param tag: Tag for which we want all values
    :return: List of all values for selected Tag
    """
    tag_query = "import \"influxdata/influxdb/v1\"\
    v1.tagValues(\
      bucket: \"Sensor_data\",\
      tag: \"{}\",\
      predicate: (r) => true,\
      start: -1y)".format(tag)
    return query_val_from_db(tag_query)


def main():
    boiler_querry = "from(bucket: \"{}\")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r._measurement == \"boiler_radiator_temp\")\
    |> filter(fn: (r) => r._field == \"tmp_in\")\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> last()".format(get_bucket(), "raspi-0000000047bf8692")
    print(query_field_val_from_db(boiler_querry))


if __name__ == "__main__":
    main()
