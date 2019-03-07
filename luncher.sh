#!/bin/bash

# file: luncher.sh
# sed -i -e 's/\r$//' luncher.sh
#----
# Simple script to start / stop a python script in the background.
#----

#----
# To Use:
# Just run: "./startstop.sh". If the process is running it will stop it or it will start it if not.
#----

#----BEGIN EDITABLE VARS----

SCRIPT_TO_EXECUTE_PLUS_ARGS='app.py -m -r'

OUTPUT_PID_FILE=running.pid

OUTPUT_PID_PATH="/home/imperium"

PYTHON_TO_USE="$(which python3)"

# If the .pid file doesn't exist (let's assume no processes are running)...
if [ ! -e "$OUTPUT_PID_PATH/$OUTPUT_PID_FILE" ]; then

	# If the running.pid file doesn't exists, create it, start PseudoChannel.py and add the PID to it.

	"$PYTHON_TO_USE" ./$SCRIPT_TO_EXECUTE_PLUS_ARGS > /dev/null 2>&1 & echo $! > "$OUTPUT_PID_PATH/$OUTPUT_PID_FILE"
	# echo $(date +'%Y-%m-%d %H:%M:%S') '|luncher|info|The service has been started|200' >> /home/tweety/log/log.txt
	echo "Started $SCRIPT_TO_EXECUTE_PLUS_ARGS @ Process: $!"

	sleep .7

	echo "Created $OUTPUT_PID_FILE file in $OUTPUT_PID_PATH dir"
	chmod 755 "$OUTPUT_PID_PATH/$OUTPUT_PID_FILE"
    echo "1" > "$OUTPUT_PID_PATH/runnable.txt"

else

	# If the running.pid exists, read it & try to kill the process if it exists, then delete it.
	the_pid=$(<$OUTPUT_PID_PATH/$OUTPUT_PID_FILE)

	rm "$OUTPUT_PID_PATH/$OUTPUT_PID_FILE"

	echo "Deleted $OUTPUT_PID_FILE file in $OUTPUT_PID_PATH dir"

	kill "$the_pid"

	COUNTER=1

	while [ -e /proc/$the_pid ]

	do

	    echo "$SCRIPT_TO_EXECUTE_PLUS_ARGS @: $the_pid is still running"

	    sleep .7

	    COUNTER=$[$COUNTER +1]

	    if [ $COUNTER -eq 20 ]; then

	    	kill -9 "$the_pid"

	    fi

	    if [ $COUNTER -eq 40 ]; then

	    	exit 1

	    fi

	done

	echo "$SCRIPT_TO_EXECUTE_PLUS_ARGS @: $the_pid has finished"
    echo "0" > "$OUTPUT_PID_PATH/runnable.txt"
    # echo $(date +'%Y-%m-%d %H:%M:%S') '|luncher|info|The service has been turned off|200' >> /home/tweety/log/log.txt
fi

exit 0