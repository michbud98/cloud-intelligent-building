docker run --rm -d --name grafana --user 472 \
--volume "$PWD/grafana_data:/var/lib/grafana" \
-p 3000:3000 \
--link influxdb_database \
grafana/grafana