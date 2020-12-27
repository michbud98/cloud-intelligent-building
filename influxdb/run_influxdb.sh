docker run --rm -d --name influxdb \
-v $PWD/database_files:/var/lib/influxdb \
-p 8086:8086 influxdb:1.8.3
