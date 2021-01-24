docker run --rm --name telegraf_test \
-v $PWD/telegraf_docker_my.conf:/etc/telegraf/telegraf.conf:ro \
-v $PWD/get_sensor_data_nodemcu.py:/etc/telegraf/get_sensor_data_nodemcu.py \
michbud98/telegraf-python:1.0 --test
