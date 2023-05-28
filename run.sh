#!/usr/bin/bash
if [ "$1" == "" ]
then 
	python3 /app/main_window.py
elif [ "$1" == "--background" ]
	then
		python3 /app/periodic_saving.py
elif [ "$1" == "--installer" ]
	then
		python3 /app/install_flatpak_from_script.py
fi
