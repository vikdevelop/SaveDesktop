#!/usr/bin/bash

if [ "$SNAP" == "" ]
then 
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
   		echo -e '\033[1mArguments:\033[0m \n None | Run SaveDesktop app (GUI) \n --background | Start periodic saving \n --sync | Sync desktop configuration with other computer \n --start-server | Start HTTP server for synchronization DE config with other computers \n --help | Show this message'
fi
else
  for plug in "dot-config" "dot-local" "dot-themes" "dot-icons" "dot-fonts" "login-session-control"; do
    if ! snapctl is-connected $plug; then
      zenity --error --text="Please open the terminal (Ctrl+Alt+T) and run the following command: \n\nsudo snap connect savedesktop:dot-config &amp;&amp; sudo snap connect savedesktop:dot-local &amp;&amp; sudo snap connect savedesktop:dot-themes &amp;&amp; sudo snap connect savedesktop:dot-icons &amp;&amp; sudo snap connect savedesktop:dot-fonts &amp;&amp; sudo snap connect savedesktop:login-session-control"
      exit
    fi
  done
  if [ "$1" == "" ]
  then 
		python3 $SNAP/usr/main_window.py
	elif [ "$1" == "--background" ]
  then
			python3 $SNAP/usr/periodic_saving.py
	elif [ "$1" == "--sync" ]
		then
			python3 $SNAP/usr/network_sharing.py
	elif [ "$1" == "--start-server" ]
		then
			python3 $SNAP/usr/server.py
	elif [ "$1" == "--help" ]
		then
		echo -e '\033[1mArguments:\033[0m \n None | Run SaveDesktop app (GUI) \n --background | Start periodic saving \n --sync | Sync desktop configuration with other computer \n --start-server | Start HTTP server for synchronization DE config with other computers \n --help | Show this message'
  fi
fi 
