docker run --rm --name grafana --user 0 \
--volume "$PWD/grafana_data:/var/lib/grafana" \
-p 3000:3000 \
--link influxdb \
grafana/grafana
