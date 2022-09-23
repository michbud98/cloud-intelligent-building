# cloud-intelligent-building
Collection of programs running inside intelligent building

InfluxDB 2.0 Cloud database url:
https://eu-central-1-1.aws.cloud2.influxdata.com/

## Initial setup of TIG on RPI4:
1. Create .env file next to docker-compose file
    - Fill it with Mariadb root password and default database name:
    ```
    MYSQL_ROOT_PASSWORD=<example>
    MARIADB_DATABASE=<example>
    ```
2. Run influxdb and grafana containers with:
```
docker-compose up influxdb grafana
```
3. Login to Influxdb using web browser with "RPI4_IP:8086" and follow initial setup steps 
    - Fill in username, password, org. name (example. [TIG]) and initial bucket name (ex. [TIG_bucket]).
    - Generate new access token for your initial bucket (Data > API Tokens) with Read/Write permissions for that bucket [TIG_TOKEN].
4. Login to Grafana using web browser with "RPI4_IP:3000"
    - On login screen use default user admin and fill in password admin
    - Set new password when prompted.
5. Go to Grafana configuration (COG icon) and add new Data source
    - Add data source type InfluxDB
    - Set query language Flux
    - Set URL to http://influxdb:8086
    - Fill in your Influxdb org. name [TIG]
    - Fill in your InfluxDB token that you generated [TIG_TOKEN]
    - Fill in your initial bucket name [TIG_bucket]
    - Save and test 
    - Import grafana dashboards from grafana folder
6. Create volume folders Telegraf and Mosquitto with:
```
docker-compose up -d telegraf mosquitto
docker-compose down
```
7. Create Telegraf config file (Prepared example file can be used in /telegraf/Main/telegraf_docker.conf)
    - For saving data to InfluxDB using telegraf you have to fill in Org. name [TIG], token [TIG_TOKEN], bucket name [TIG_bucket] in outputs.influxdb_v2 plugin configuration
    - NAME FINAL CONFIG FILE [telegraf.conf]
    - Copy this config file in volumes/telegraf (use sudo cp):
    - Copy any scripts for data collection alongside telegraf.conf to the volume (Example in telegraf/Wi-Fi/scrap-scripts/luftdaten_scrap.py)
8. Create mosquitto config file (Prepared example file can be used in /telegraf/MQTT/mosquitto.conf)
    - Copy this config file in volumes/mosquitto/config/ (use sudo cp)
9. Run Nodered container and open console inside with:
```
docker-compose up -d nodered
docker exec -it nodered /bin/bash
```
10. Generate your password hash with:
```
node-red admin hash-pw
```
Save your hashed admin pasword [admin_passwd] for later then exit container.

11. Create new Nodered settings file (Example in nodered/settings_docker.js) and save your hashed password [admin_passwd] in admin credentials (ctrl-f [adminAuth])
    - NAME FINAL FILE [settings.js]
    - Save settings file in volumes/nodered/data (use sudo cp)
12. Run Nodered container again with:
```
docker-compose up
```
13. Import Flows from JSON files in folder nodered/
    - Run function Create sensors table

After all these steps you can run TIG detached by commands:
- Docker-compose up -d


## Used resources:
### Raspberry pi Enviro Plus sensor library by pimoroni
- https://github.com/pimoroni/enviroplus-python

### Raspberry pi BME680 sensor library by pimoroni
- https://github.com/pimoroni/bme680-python

### Nodemcu with BME280 sensor installation guide by sensor.community
- https://sensor.community/en/sensors/airrohr/

