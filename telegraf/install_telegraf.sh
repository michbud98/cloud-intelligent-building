DEBUG=0
HOSTNAME=""
INFLUX_HOST=""
INFLUX_TOKEN=""
INFLUX_ORG=""
INFLUX_BUCKET="" 

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
	cp -f telegraf_sensor_data.conf /etc/telegraf/telegraf.conf
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot replace default config file at /etc/telegraf/telegraf.conf"
	else
		echo "SUCCESS: Config at /etc/telegraf/telegraf.conf replaced"
	fi

	echo "Placing custom python script to telegraf config dir"
	cp /python_scripts/raspberry_pi_save_weather_stats/get_weather_data.py /etc/telegraf/
	RC=$?	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot place python script in telegraf config directory /etc/telegraf"
	else
		echo "SUCCESS: get_weather_data.py placed in /etc/telegraf/get_weather_data.py"
	fi

	echo "Changing get_weather_data.py ownership to pi"
	chown pi /etc/telegraf/get_weather_data.py && chgrp pi /etc/telegraf/get_weather_data.py
	RC=$?
	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot change ownership of get_weather_data.py to user pi"
	else	
		echo "SUCCESS: Ownership of file get_weather_data changed to user pi"
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

# Gets necessary env variables for connection to influx cloud from user
enter_env_var_values()
{
	echo "Creating file for enviromental variables"
	[ $DEBUG -eq 1 ] && set -x
	# Methods obtaining values of influx env variables from user
	enter_sensor_name
	enter_influx_host
	enter_influx_token
	enter_influx_org
	enter_influx_bucket	

	# Last comfirmation before saving into /etc/default/telegraf
	comfirm_env_var_values
	
}

# Saves env variables to /etc/default/telegraf
save_env_var_values()
{
	[ $DEBUG -eq 1 ] && set -x
	set -e
	echo "Overwriting default telegraf env variables file at /etc/default/telegraf with your env variables"
	echo "HOSTNAME=\"$HOSTNAME\"" | sudo tee /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write HOSTNAME to /etc/default/telegraf"
	else	
		echo "SUCCESS: HOSTNAME written to /etc/default/telegraf"
	fi

	echo "INFLUX_HOST=\"$INFLUX_HOST\"" | sudo tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_HOST to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_HOST written to /etc/default/telegraf"
	fi

	echo "INFLUX_TOKEN=\"$INFLUX_TOKEN\"" | sudo tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_TOKEN to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_TOKEN written to /etc/default/telegraf"
	fi

	echo "INFLUX_ORG=\"$INFLUX_ORG\"" | sudo tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_ORG to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_ORG written to /etc/default/telegraf"
	fi

	echo "INFLUX_BUCKET=\"$INFLUX_BUCKET\"" | sudo tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_BUCKET to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_BUCKET written to /etc/default/telegraf"
	fi
	
	echo "Installation successfull"
	echo "RECOMMENDATION: Reboot sensor for telegraf config to take effect"
}

# Prints entered env variables values and request last cmfirmation before saving
comfirm_env_var_values()
{
	while true; do

		if [ -z "$HOSTNAME" ]; then
			printf "Variables saved in file /etc/default/telegraf
			Sensor hostname [HOSTNAME]: Default value
			Influx host adress [INFLUX_HOST]: $INFLUX_HOST
			Influx token [INFLUX_TOKEN]: $INFLUX_TOKEN
			Influx organization [INFLUX_ORG]: $INFLUX_ORG
			Influx bucket [INFLUX_BUCKET]: $INFLUX_BUCKET \n"
		else
			printf "Variables saved in file /etc/default/telegraf
			Sensor hostname [HOSTNAME]: $HOSTNAME
			Influx host adress [INFLUX_HOST]: $INFLUX_HOST
			Influx token [INFLUX_TOKEN]: $INFLUX_TOKEN
			Influx organization [INFLUX_ORG]: $INFLUX_ORG
			Influx bucket [INFLUX_BUCKET]: $INFLUX_BUCKET \n"
		fi
		read -p "Change Sensor (H)ostname, Influx host (A)ddress, (T)oken, (O)rganization, (B)ucket, (R)esume, (E)nd program: " USER_INPUT
		USER_INPUT=$(echo $USER_INPUT | tr '[:upper:]' '[:lower:]')

		case "$USER_INPUT" in
			h) enter_sensor_name ;;
			a) enter_influx_host ;;
			t) enter_influx_token ;;
			o) enter_influx_org ;;
			b) enter_influx_bucket ;;
			r) 
			# This method saves env variables to /etc/default/telegraf
			save_env_var_values
			break ;;
			e) 
			echo "Closing program. You can later edit /etc/default/telegraf to add env variables for telegraf config"
			exit 0 ;;
			\?) 
			echo "Wrong argument. Please try again."
			continue ;;
		esac
	done
}

# Setting hostname for sensor
# On empty string uses default value
enter_sensor_name()
{
	while true; do
		read -p "Enter sensor hostname [HOSTNAME] (Default used on empty string) : " HOSTNAME
		if [ -z "$HOSTNAME" ]; then
			echo "You entered empty string. Default hostname will be used."
		else
			echo "You entered value [$HOSTNAME] as sensor name"
		fi
		read -p "Is this correct [y/n]? " USER_INPUT
		USER_INPUT=$(echo $USER_INPUT | tr '[:upper:]' '[:lower:]')
		if [ $USER_INPUT = "y" ]; then
			break
		elif [ $USER_INPUT = "n" ]; then
			continue
		fi

	done
}

# Checks if value is not empty and requests user to comfirm value which he entered
# arg1 env variable value
# arg2 written name of env variable
# Return 0 (true) or 1 (false) which is used by other methods
enter_value_check()
{
	arg1=$1
	arg2=$2

	if [ -z "$arg1" ]; then
		echo "ERROR: $2 cant be empty. Type it again."
		return 1
	fi
	echo "You entered value [$arg1] as $arg2"
	read -p "Is this correct [y/n]? " USER_INPUT
	USER_INPUT=$(echo $USER_INPUT | tr '[:upper:]' '[:lower:]')
	if [ $USER_INPUT = "y" ]; then
		return 0
	elif [ $USER_INPUT = "n" ]; then
		return 1
	fi
}

enter_influx_host()
{
	while true; do
		read -p "Enter influx host address [INFLUX_HOST]: " INFLUX_HOST
		enter_value_check "$INFLUX_HOST" "Influx host adress"
		RC=$? # read return code from function
		[ $RC -eq 0 ] && break
	done
}


enter_influx_token()
{
	while true; do
		read -p "Enter influx token [INFLUX_TOKEN]: " INFLUX_TOKEN
		enter_value_check "$INFLUX_TOKEN" "Influx token"
		RC=$?
		[ $RC -eq 0 ] && break
	done
}

enter_influx_org()
{
	while true; do
		read -p "Enter influx organization [INFLUX_ORG]: " INFLUX_ORG
		enter_value_check "$INFLUX_ORG" "Influx organization"
		RC=$?
		[ $RC -eq 0 ] && break
	done
}

enter_influx_bucket()
{
	while true; do
		read -p "Enter influx bucket name [INFLUX_BUCKET]: " INFLUX_BUCKET
		enter_value_check "$INFLUX_BUCKET" "Influx bucket name"
		RC=$?
		[ $RC -eq 0 ] && break
	done
}

# Prints help
usage()
{
	echo "install_telegraf.sh [-dh]"
}

while getopts dh Opt; do
  case "$Opt" in
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
# Encapsulates Methods obtaining values of influx env variables from user 
enter_env_var_values


