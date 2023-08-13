#!/usr/bin/bash
if [ "$1" == "" ]
then 
	python3 /app/main_window.py
elif [ "$1" == "--background" ]
	then
		python3 /app/periodic_saving.py
elif [ "$1" == "--sync" ]
	then
		python3 /app/network_sharing.py
elif [ "$1" == "--start-server" ]
	then
		python3 /app/server.py
fi
