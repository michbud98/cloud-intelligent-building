docker run --rm -d --name telegraf \
-v $PWD/telegraf_docker_my.conf:/etc/telegraf/telegraf.conf:ro \
-v $PWD/luftdaten_scrap.py:/etc/telegraf/luftdaten_scrap.py \
-v $PWD/pocasidoma_meteo_scrap.py:/etc/telegraf/pocasidoma_meteo_scrap.py \
michbud98/telegraf-python:1.0
