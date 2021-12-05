FROM eclipse-mosquitto
COPY mosquitto.conf /mosquitto/config/mosquitto.conf
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]