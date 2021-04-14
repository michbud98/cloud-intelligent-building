# cloud-intelligent-building
Collection of programs running inside intelligent building

InfluxDB 2.0 Cloud database url:
https://eu-central-1-1.aws.cloud2.influxdata.com/

Grafana cloud url:
https://intelligentbuilding2.grafana.net/

## How to run
### TIG on local machine
```
docker-compose up
```

### Django control web app on local machine
```
cd django
docker-compose up
```

### Dummy machines
```
cd dummy_machines
docker build -t <docker image name> .
docker run --rm --network="host" <docker image name> -s 5 -url http://localhost:<port of control app> Thermometer 1
```

## Used resources:
### Raspberry pi Enviro Plus sensor library by pimoroni
- https://github.com/pimoroni/enviroplus-python

### Raspberry pi BME680 sensor library by pimoroni
- https://github.com/pimoroni/bme680-python

### Nodemcu with BME280 sensor installation guide by sensor.community
- https://sensor.community/en/sensors/airrohr/

