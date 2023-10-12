#!/usr/bin/bash
cd ~/.local/share/savedesktop
if [ "$1" == "" ]
then 
	python3 src/main_window.py
elif [ "$1" == "--background" ]
	then
		python3 src/periodic_saving.py
elif [ "$1" == "--sync" ]
	then
		python3 src/network_sharing.py
elif [ "$1" == "--start-server" ]
	then
		python3 src/server.py
elif [ "$1" == "--update" ]
	then
		python3 ~/.local/bin/native_updater.py
elif [ "$1" == "--help" ]
	then
   		echo -e '\033[1mArguments:\033[0m \n None | Run SaveDesktop app (GUI) \n --background | Start periodic saving \n --sync | Sync desktop configuration with other computer \n --start-server | Start HTTP server for synchronization DE config with other computers \n --help | Show this message'
fi

cd
