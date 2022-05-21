FROM telegraf

RUN mkdir /home/root
WORKDIR /home/root


# COPY ./telegraf_docker_my.conf /etc/telegraf/telegraf.conf:ro
# COPY ./luftdaten_scrap.py /etc/telegraf/luftdaten_scrap.py
# COPY ./pocasidoma_meteo_scrap.py /etc/telegraf/pocasidoma_meteo_scrap.py

RUN apt-get update && apt-get install python3 python3-pip -y
RUN pip3 install requests beautifulsoup4

#"/bin/bash"
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "telegraf" ]