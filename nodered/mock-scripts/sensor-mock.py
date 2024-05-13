import requests
import json
import random
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("sensor_id")
args = parser.parse_args()

url = "http://127.0.0.1:1880/postSensor"
while(True):

    payload = json.dumps({
        "sensor_id": args.sensor_id,
        "board_type": args.sensor_id.split('-')[0],
        "sensor_type": "BME680",
        "temperature": random.randrange(0,30),
        "pressure": random.randrange(0,1000),
        "humidity": random.randrange(0,100)
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    time.sleep(60)
