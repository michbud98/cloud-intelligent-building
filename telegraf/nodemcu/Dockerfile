FROM telegraf

RUN mkdir /home/root
WORKDIR /home/root

RUN apt-get update && apt-get install python3 python3-pip -y
RUN pip3 install requests beautifulsoup4

#"/bin/bash"
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "telegraf" ]