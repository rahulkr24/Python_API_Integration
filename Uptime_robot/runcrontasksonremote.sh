#!/bin/bash


# Utility functions

cron_time_func()
{
	VAL=60
	NULL=0
	MINUTE=$1
	if [ "$MINUTE" -ge "$VAL" ];
	then
		TOTAL_HOUR=$(($MINUTE / $VAL))
		TOTAL_MINUTE=$(($MINUTE % $VAL))
	else
		TOTAL_MINUTE=$MINUTE
		TOTAL_HOUR=$NULL
	fi
	
	if [ "${TOTAL_MINUTE}" != "${NULL}" ] && [ "${TOTAL_HOUR}" == "${NULL}" ];
	then
		echo "*/${TOTAL_MINUTE} * * * *"
	elif [ "${TOTAL_HOUR}" != "${NULL}" ] && [ "${TOTAL_MINUTE}" == "${NULL}" ];
		then
			if [ "${TOTAL_HOUR}" == 1 ];
			then
				TOTAL_HOUR=0
				echo "${TOTAL_HOUR} * * * *"
			else
				echo "0 */${TOTAL_HOUR} * * * "
			fi
	elif [ "${TOTAL_HOUR}" != "${NULL}" ] && [ "${TOTAL_MINUTE}" != "${NULL}" ];
	then
		echo "${TOTAL_MINUTE} */${TOTAL_HOUR} * * *"
	else
		echo "* * * * *"
	fi
}



extension_path()
{
	FILE_EXTENSION=$1
	if [[ ${FILE_EXTENSION: -3} == ".sh" ]]
	then
		EXECUTER=$(which bash)
	elif [[ ${FILE_EXTENSION: -3} == ".py" ]]
	then 
		EXECUTER=$(which python3)
	else
		echo "ENTER THE VALID FILE NAME"
	fi
	echo $EXECUTER
}



create_crontab()
{

	FILE_NAME=$1
	if [ -z "$FILE_NAME" ]
	then
		echo "Filename Param missing. Exiting ..."
		exit
	fi

	TIME=$2
	if [ -z "$TIME" ]
	then
		echo ${TIME}
		echo "Cron Delay internal parameter missing. Exiting ..."
		exit

	else
		if ! [[ "${TIME}" =~ ^[0-9]+$ ]];
		then
		    echo "Cron time paprameter must be all integers or 'RunOnceOnReboot' only. Exiting ..."
		    exit
		fi
	fi


	if [ "$TIME" == RunOnceOnReboot ];
	then
		TIMER="@reboot sleep 20 &&"
	else
		TIMER=$(cron_time_func $TIME)
	fi

	echo 
	echo "FILE_NAME: [$FILE_NAME] CRON_TIME: [$TIME] Crontab TIMER: [$TIMER]"
	echo

	EXTENSION=$(extension_path $FILE_NAME)

	export val_dir=$PWD 
	LOGS=">> ${val_dir}/output_of_${FILE_NAME::-3}.log 2>&1"
	LOG=">> ${val_dir}/${FILE_NAME::-3}.log"
	FILE=./${FILE_NAME}
	CLEANUP_FILE=./cleanup_dumps.sh

	if [ -f "$FILE" ]; then
	    echo "$FILE exists."

	    echo
		echo "${TIMER} ${EXTENSION} ${FILE}"
		echo
		# * * * * * if /opt/cpanel/ea-php73/root/usr/bin/php /home/company/example.de/bin/magento list >/dev/null 2>&1; then echo ran successfully; else echo failed; fi >>/home/company/example.de/var/log/test.cron.log

		crontab -l > cron_backup	
		echo "${TIMER} cd $val_dir && if ${EXTENSION} ${FILE} ${LOGS}; then echo \$(date +\%Y-\%m-\%d_\%H-\%M) ${FILE_NAME} ran successfully; else echo \$(date +\%Y-\%m-\%d_\%H-\%M) ${FILE_NAME} failed to run; fi ${LOG}" >> cron_backup
		crontab cron_backup

	else 
	    echo "$FILE does not exist."
	fi

}


# **************************************************
# Enter Reboot to run the script run one time after reboot

# Enter 0 to run every minute

# Format (FILE_NAME and CRON_TIME)
#               \           /
#                \         /
# create_crontab test1.py 0

echo
# echo "*** SETTING UP AIRTABLE EXPORT ***"
# create_crontab airtableexport.sh 5

# echo
# echo "*** SETTING UP POSTGRES DB BACKUP ***"
# create_crontab backup.sh 60
create_crontab create_monitor.py 10
echo