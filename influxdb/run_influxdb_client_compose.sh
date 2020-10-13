docker run --rm -it --network=sensor_monitor_default --name influxdb_client \
--link=influxdb_database influxdb influx -host influxdb_database 