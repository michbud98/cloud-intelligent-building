DEBUG=0

# Installs configuration files and replaces default telegraf service on raspberry pi 
install_configuration()
{
	[ $DEBUG -eq 1 ] && set -x
	
	echo "Creating directory for service script"
	Script_file="get_sensor_data_1wire.py"
	Homedir="/home/pi/boiler_data_collect"
	mkdir $Homedir
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot create dir $Homedir"
	else
		echo "SUCCESS: Created dir $Homedir"
	fi

	echo "Replacing default telegraf service file with modified telegraf service file"
	Route="/etc/systemd/system/"
	cp -f get_sensor_data.service $Route
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot replace default telegraf service file at $Route"
	else
		echo "SUCCESS: Service $Route"
	fi

	echo "Placing custom python script to telegraf config dir"
	cp get_sensor_data_1wire.py $Homedir/$Script_file
	RC=$?	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot place python script in $Homedir/$Script_file"
	else
		echo "SUCCESS: get_sensor_data_1wire.py placed in $Homedir/$Script_file"
	fi

	echo "Changing get_sensor_data_1wire.py ownership to pi"
	chown pi $Homedir/$Script_file && chgrp pi $Homedir/$Script_file
	RC=$?
	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot change ownership of $Homedir/$Script_file to user pi"
	else	
		echo "SUCCESS: Ownership of file $Homedir/$Script_file changed to user pi"
	fi

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

# Install telegraf configuration and scripts at /etc/telegraf
install_configuration
echo "Enable service with sudo systemctl enable get_sensor_data.service"


