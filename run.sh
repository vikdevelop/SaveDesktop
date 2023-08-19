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
elif [ "$1" == "--help" ]
	then
   		echo -e '\033[1mArguments:\033[0m\n --background | Start periodic saving \n --sync | Sync desktop configuration with other computer \n --start-server | Start HTTP server for synchronization DE config with other computers \n --help | Show this message'
fi
