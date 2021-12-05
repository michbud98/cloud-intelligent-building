docker run --rm \
-v $PWD/influx_recovery_file_my.conf:/etc/telegraf/telegraf.conf:ro \
-v $PWD/telegraf_logs:/tmp/ \
michbud98/telegraf-recovery