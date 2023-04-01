#!/usr/bin/bash
if [ "$1" == "" ]
then 
	python3 /app/main_window.py
elif [ "$1" == "--background" ]
	then
		python3 /app/periodic_saving.py
fi
