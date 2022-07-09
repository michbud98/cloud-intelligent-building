#!/usr/bin/env python3

import requests

# Read values from METEO
def read_meteo():
    value_names = ["Vítr směr", "Tlak relat.", "Vlhkost ven.", "Teplota ven.", "Intenzita srážek", "Déšť"]
    values = {}
    http="http://www.pocasidoma.cz/?ajax=getDetailMarker&idstation=360"
    
    req = requests.get(http)
    # print("Status: {}".format(req.status_code))
    values["status"] = req.status_code
    #print("Text: {}".format(req.text))
    #meteo = json.dumps(req.json())
    meteo = req.json()
    values["id"] = meteo["Data"]["id"]
    # print(f"----------METEO----------\r\n {meteo}")
    meteo_val = meteo["Data"]["allMeasures"]
    # print(meteo)
    
    for value in meteo_val:
        if value["Name"] in value_names:
            # print("{}:    {}".format(value["Name"],value["Value"]))
            values[value["Name"]] = value["Value"]
    return values

def main():
    values = read_meteo()
    board_type = "pocasidoma"
    sensor_id = "{}-{}".format(board_type, values["id"])
    temp_arg = values["Teplota ven."]
    pres_arg = values["Tlak relat."]
    hum_arg = values["Vlhkost ven."]

    print("sensor_data,sensor_id={0},board_type={1},room=Outdoors,comm_protocol=Scrap temperature={2},pressure={3},humidity={4}".format(
    sensor_id, board_type, temp_arg, pres_arg, hum_arg))


if __name__ == "__main__":
    main()