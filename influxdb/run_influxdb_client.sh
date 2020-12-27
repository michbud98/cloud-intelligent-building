docker run --rm -it --name influxdb_client \
--link=influxdb influxdb:1.8.3 influx -host influxdb
