FROM eclipse-mosquitto:2.0.11
COPY mosquitto.conf /mosquitto/config/mosquitto.conf
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]