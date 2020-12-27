docker run --rm -it --network=cloud-intelligent-building_default --name influxdb_client \
--link=influxdb influxdb:1.8.3 influx -host influxdb
