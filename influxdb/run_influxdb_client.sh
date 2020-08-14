docker run --rm -it --name influxdb_client \
--link=influxdb_database influxdb influx -host influxdb_database 