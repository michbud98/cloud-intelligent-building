FROM telegraf

RUN mkdir /home/root
WORKDIR /home/root


#COPY ./telegraf_docker_my.conf /etc/telegraf/telegraf.conf:ro
#COPY ./get_sensor_data_nodemcu.py /etc/telegraf/get_sensor_data_nodemcu.py
# Map Volumes
# $PWD/telegraf/nodemcu/telegraf_docker_my.conf:/etc/telegraf/telegraf.conf:ro
# $PWD/telegraf/nodemcu/get_sensor_data_nodemcu.py:/etc/telegraf/get_sensor_data_nodemcu.py

RUN apt-get update && apt-get install python3 python3-pip -y
RUN pip3 install requests beautifulsoup4

#"/bin/bash"
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "telegraf" ]