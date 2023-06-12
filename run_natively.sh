#!/usr/bin/bash
cd ~/.local/share/savedesktop
if [ "$1" == "" ]
then 
	python3 src/main_window.py
elif [ "$1" == "--background" ]
	then
		echo "Periodic saving is currently only supported in Flatpak."
fi

cd
