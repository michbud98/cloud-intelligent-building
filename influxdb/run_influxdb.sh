docker run --rm -d --name influxdb_database \
-v $PWD/database_files:/var/lib/influxdb \
-p 8086:8086 influxdb