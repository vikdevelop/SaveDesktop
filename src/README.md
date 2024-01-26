# Navigation
In this directory is located the most important part of the app, which is its source code.
Because there are a lot of files, this README helps you with navigate in this directory:

- `backup_flatpaks.sh` - saving Flatpak applications to a list in the configuration archive
- `config.py` - saving and importing user configuration from and in the configuration archive
- `install_flatpak_from_script.py` - installing Flatpak apps from the list to the system and copying user data from the configuration archive to the ~/.var/app directory
- `localization.py` - Based on the detected system language, the application sets the interface language (if the system language is not in the list of available languages, English is set), also sets the cache and application data folders and also the application version and release notes
- `main_window.py` - the GUI of the app
- `network_sharing.py` - synchronization between computers in the network within Python HTTP server
- `open_wiki.py` - opening the Github wiki of this app in the system language (if it is not available in the list of available languages, English opens)
- `periodic_saving.py` - saving configuration periodically
- `server.py` - starting Python HTTP server for synchronization between computers in the network
- `shortcuts_window.py` - showing available Keyboard shortcuts in the window
