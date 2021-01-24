import influxdb_client
from typing import Dict, List, Tuple

bucket = "Sensor_data"
org = "swiftblade1982@gmail.com"
token = "IqVLx0CNb_rm4yh1nebq8x70acTQ0XXMKegq5y98c-d9CK7mc5gyh1qrKrwOQHs52TKD2Nt3D3-GdeZl7ZtKaQ=="
# Store the URL of your InfluxDB instance
url="https://eu-central-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

# light_indoors_query= 'from(bucket: "Sensor_data")\
#     |> range(start: -1h)\
#     |> filter(fn: (r) => r["_measurement"] == "sensor_light")\
#     |> filter(fn: (r) => r["_field"] == "light")\
#     |> filter(fn: (r) => r["host"] == "raspberrypi")\
#     |> last()'

def query_data_from_influxdb(query) -> List[tuple]:
  result = client.query_api().query(org=org, query=query)
  results = []
  for table in result:
    for record in table.records:
      results.append((record.get_field(), record.get_value()))

  return results

# print(query_data_from_influxdb(light_indoors_query))
