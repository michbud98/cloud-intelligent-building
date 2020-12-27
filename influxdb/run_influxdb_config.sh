docker run --rm -d --name influxdb \
-v $PWD/database_files:/var/lib/influxdb \
-v $PWD/config_files/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
-p 8086:8086 \
influxdb:1.8.3 -config /etc/influxdb/influxdb.conf
