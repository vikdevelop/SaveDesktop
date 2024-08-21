#!/usr/bin/bash
CACHE=${HOME}/.cache/io.github.vikdevelop.SaveDesktop
cd ~/.local/share/savedesktop
if [ "$1" == "" ]; then
    python3 src/main_window.py
elif [ "$1" == "--background" ]; then
    python3 src/periodic_saving.py
elif [ "$1" == "--save-now" ]; then
    python3 src/periodic_saving.py --now
elif [ "$1" == "--sync" ]; then
    python3 src/network_sharing.py
elif [ "$1" == "--start-server" ]; then
    python3 src/server.py
elif [ "$1" == "--update" ]; then
    python3 ~/.local/bin/native_updater.py
elif [ "$1" == "--import-config" ]; then
    echo -e '{\n "import_file": "'$2'"\n}'> $CACHE/.impfile.json
    mkdir $CACHE/import_config
    rm -rf $CACHE/import_config/*
    cd $CACHE/import_config
		if [[ "$2" == *.sd.tar.gz ]]; then
				echo "decompressing Tar archive"
		elif [[ "$2" == *.sd.zip ]]; then
				echo "decrypting zip archive"
				unzip -o "$2"
		else
				echo "You are selected an unsupported file type. The supported files are: *.sd.tar.gz and *.sd.zip"
				exit
		fi
    python3 ~/.local/share/savedesktop/src/config.py --import_
elif [ "$1" == "--help" ]; then
    echo -e '\033[1mArguments:\033[0m \n None | Run SaveDesktop app (GUI) \n --background | Start periodic saving \n --sync | Sync desktop configuration with other computer \n --start-server | Start HTTP server for synchronization DE config with other computers \n --import-config /path/to/filename.sd.tar.gz | Import configuration of DE \n --save-now | Save configuration of DE using parameters from UI\n --help | Show this message'
fi

cd
