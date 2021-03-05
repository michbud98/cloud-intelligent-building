from enum import Enum
import random
import requests
from urllib.parse import urlparse, ParseResult



blinds = [f'B{i}' for i in range(0, 5)]
thermometers = [f'T{i}' for i in range(0, 5)]

random.seed(2)

class DeviceType(Enum):
    BLINDS = "Blinds"
    THERMOMETERS = "Thermo"

def make_request(django_url: str = "http://localhost:8000", device_type: DeviceType = DeviceType.BLINDS, id: int = -1):
    if(device_type == DeviceType.BLINDS):
        if(id == -1):
            id = random.randint(0, len(blinds)-1)
        id: str = blinds[id]
    elif(device_type == DeviceType.THERMOMETERS):
        if(id == -1):
            id = random.randint(0, len(thermometers)-1)
        id: str = thermometers[id]

    url: str = django_url + f'/devices/{id}/get_value'
    print(f"URL: {url}")
    res = requests.get(url)
    print(res)
    if res.status_code == 200:
        value = res.json()
        if(device_type == DeviceType.BLINDS):
            print(f"Sunblind {id}: {value['data']}")
        elif(device_type == DeviceType.THERMOMETERS):
            print(f"Thermometer {id}: {value['data']}")