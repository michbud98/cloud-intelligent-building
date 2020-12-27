FROM arm32v7/debian

RUN mkdir /home/root
WORKDIR /home/root

COPY influxdb2-2.0.3_linux_arm64 .

ENTRYPOINT [ "/entrypoint.sh" ]
