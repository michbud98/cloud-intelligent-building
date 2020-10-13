docker run -d --rm --name telegraf \
-v $PWD/telegraf_docker.conf:/etc/telegraf/telegraf.conf:ro \
--privileged -v /:/hostfs:ro -e HOST_MOUNT_PREFIX=/hostfs -e HOST_PROC=/hostfs/proc \
--link influxdb_database \
telegraf