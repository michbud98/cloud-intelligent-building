# Sensor-stack
Sensor stack for Raspberry Pi 4 that collects data from sensors and saves it to database for further analysis.
Stack consists of:
- TimescaleDB (Postgresql) for storing data
- Nodered for data processing
- Grafana for data visualization


## Initial setup manually on RPI4:
1. Create .env file next to docker-compose file
    - Fill it with password for TimescaleDB user (same as in Postgresql):
    ```
    POSTGRES_PASSWORD=example
    ```

2. Run Nodered container and open console inside with:
    ```
    docker run --rm -d --name "passwd-nodered" nodered/node-red
    docker exec -it passwd-nodered /bin/bash
    ```

3. Generate your password hash with:
    ```
    node-red admin hash-pw
    ```

4. Update nodered settings.js (nodered/settings_docker.js) and save your hashed password [admin_passwd] in admin credentials (ctrl-f [adminAuth]). After that you can exit the container with:
    ```
    docker stop passwd-nodered
    ```

5. Run docker-compose:
    ```
    docker-compose up -d
    # (or with --build if you want to rebuild images)
    docker-compose up -d --build
    ```

6. Login to Grafana using web browser with "RPI4_IP:3000"
    - On login screen use default user "admin" and fill in default password "admin"
    - Set new password when prompted.

7. Go to Grafana configuration and add new Data source
    - Add data source type PostgreSQL
    - Set URL to timescaledb:5432
    - Fill in database name, user with "postgres" and password from .env file
    - Disable TLS/SSL mode
    - Turn on TimescaleDB
    - Save and test 

8. Import grafana dashboards from grafana folder
    - Go to Grafana and import dashboard
    - Choose JSON file from grafana folder
    - Set data source to TimescaleDB
    - Import
    - It is possible that you will need to adjust data source in queries and fill variable Room with query "SELECT room FROM sensor_measurements;". Also you need to adjust refresh each query in panel by adding and removing latter and then running the query.



## Used resources:
### Raspberry pi Enviro Plus sensor library by pimoroni
- https://github.com/pimoroni/enviroplus-python

### Raspberry pi BME680 sensor library by pimoroni
- https://github.com/pimoroni/bme680-python

### Nodemcu with BME280 sensor installation guide by sensor.community
- https://sensor.community/en/sensors/airrohr/

