docker run --rm -d --name telegraf \
-v $PWD/telegraf_docker_my.conf:/etc/telegraf/telegraf.conf:ro \
-v $PWD/get_weather_data_nodemcu.py:/etc/telegraf/get_weather_data_nodemcu.py \
michbud98/telegraf-python:1.0
