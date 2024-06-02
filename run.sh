#!/usr/bin/bash

CACHE=${HOME}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp/
CACHE_SNAP=$SNAP_USER_COMMON/.cache/tmp

if [ "$SNAP" == "" ]; then
    if [ "$1" == "" ]; then
        python3 /app/main_window.py
    elif [ "$1" == "--background" ]; then
        python3 /app/periodic_saving.py
    elif [ "$1" == "--save-now" ]; then
        python3 /app/periodic_saving.py --now
    elif [ "$1" == "--sync" ]; then
        python3 /app/network_sharing.py
    elif [ "$1" == "--start-server" ]; then
        python3 /app/server.py
    elif [ "$1" == "--import-config" ]; then
        echo -e '{\n "import_file": "'$2'"\n}'> $CACHE/.impfile.json
        mkdir $CACHE/import_config
        rm -rf $CACHE/import_config/*
        cd $CACHE/import_config
        python3 /app/config.py --import_
    elif [ "$1" == "--help" ]; then
        echo -e '\033[1mArguments:\033[0m \n None | Run SaveDesktop app (GUI) \n --background | Start periodic saving \n --sync | Sync desktop configuration with other computer \n --start-server | Start HTTP server for synchronization DE config with other computers \n --import-config /path/to/filename.sd.tar.gz | Import configuration of DE \n --save-now | Save configuration of DE using parameters from UI\n --help | Show this message'
    fi
else
    if [ "$1" == "" ]; then
        python3 $SNAP/usr/main_window.py
    elif [ "$1" == "--background" ]; then
        python3 $SNAP/usr/periodic_saving.py
    elif [ "$1" == "--save-now" ]; then
        python3 $SNAP/usr/periodic_saving.py --now
    elif [ "$1" == "--sync" ]; then
        python3 $SNAP/usr/network_sharing.py
    elif [ "$1" == "--start-server" ]; then
        python3 $SNAP/usr/server.py
    elif [ "$1" == "--import-config" ]; then
        echo -e '{\n "import_file": "'$2'"\n}'> $CACHE/.impfile.json
        mkdir $CACHE_SNAP/import_config
        rm -rf $CACHE_SNAP/import_config/*
        cd $CACHE_SNAP/import_config
        python3 $SNAP/usr/config.py --import_
    elif [ "$1" == "--help" ]; then
        echo -e '\033[1mArguments:\033[0m \n None | Run SaveDesktop app (GUI) \n --background | Start periodic saving \n --sync | Sync desktop configuration with other computer \n --start-server | Start HTTP server for synchronization DE config with other computers \n --import-config /path/to/filename.sd.tar.gz | Import configuration of DE \n --save-now | Save configuration of DE using parameters from UI\n --help | Show this message'
    fi
fi
