DEBUG=0

# Installs telegraf on raspberry pi 
install_telegraf()
{
	echo "Installing telegraf"
	[ $DEBUG -eq 1 ] && set -x
	apt-get update

	# Add the InfluxData key
	curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
	echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

	apt-get update && apt-get install telegraf
}

# Installs configuration files and replaces default telegraf service on raspberry pi 
install_configuration()
{
	[ $DEBUG -eq 1 ] && set -x
	echo "Replacing default telegraf service file with modified telegraf service file"
	cp -f telegraf.service /etc/systemd/system/multi-user.target.wants/telegraf.service
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot replace default telegraf service file at /etc/systemd/system/multi-user.target.wants/telegraf.service"
	else
		echo "SUCCESS: Service /etc/systemd/system/multi-user.target.wants/telegraf.service modified"
	fi

	echo "Replacing default config file with sensor data config file"
	cp -f telegraf_sensor_data_my.conf /etc/telegraf/telegraf.conf
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot replace default config file at /etc/telegraf/telegraf.conf"
	else
		echo "SUCCESS: Config at /etc/telegraf/telegraf.conf replaced"
	fi

	echo "Placing custom python script to telegraf config dir"
	cp get_sensor_data_bme680.py /etc/telegraf/
	RC=$?	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot place python script in telegraf config directory /etc/telegraf"
	else
		echo "SUCCESS: get_sensor_data_bme680.py placed in /etc/telegraf/get_sensor_data_bme680.py"
	fi

	echo "Changing get_sensor_data_bme680.py ownership to pi"
	chown pi /etc/telegraf/get_sensor_data_bme680.py && chgrp pi /etc/telegraf/get_sensor_data_bme680.py
	RC=$?
	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot change ownership of get_sensor_data_bme680.py to user pi"
	else	
		echo "SUCCESS: Ownership of file get_sensor_data_bme680 changed to user pi"
	fi
	
	echo "Creating log file at /var/log/telegraf"
	touch /var/log/telegraf/telegraf.log
	RC=$?

	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot create log file at /var/log/telegraf"
	else	
		echo "SUCCESS: Log file created at /var/log/telegraf"
	fi

	echo "Changing default logging directory /var/log/telegraf ownership to pi"
	chown -R pi /var/log/telegraf && chgrp -R pi /var/log/telegraf
	RC=$?

	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot change ownership of logging directory /var/log/telegraf to user pi"
	else	
		echo "SUCCESS: Ownership of logging directory /var/log/telegraf  changed to user pi"
	fi

}

# Prints help
usage()
{
	echo "install_telegraf.sh [-dh] [c] <copy conf files to /var/log/telegraf> [i] install telegraf"
}

while getopts cdhi Opt; do
  case "$Opt" in
	i) echo "Installing telegraf"
		install_telegraf
		exit 0 ;;
	c) echo "Installing configuration and necessary files"
		install_configuration
		exit 0 ;;
    d)  DEBUG=1 ;;
    h)  usage
        exit 0 ;;
    \?) usage; exit 1 ;;
  esac
done
shift `expr $OPTIND - 1`

# Install telegraf on sensor
install_telegraf
# Install telegraf configuration and scripts at /etc/telegraf
install_configuration

