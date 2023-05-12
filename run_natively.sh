#!/usr/bin/bash
#git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop
cd /tmp/SaveDesktop
if [ "$1" == "" ]
then 
	python3 src/main_window.py
elif [ "$1" == "--background" ]
	then
		echo "Periodic saving is currently only supported on Flatpak."
fi

cd
rm -rf /tmp/SaveDesktop
