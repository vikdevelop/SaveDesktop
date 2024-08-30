# Navigation
In this directory is located the most important part of the app, which is its source code.
Because there are a lot of files, this README helps you with navigate in this directory:

- `config.py` - saving and importing user configuration from and in the configuration archive
- `flatpak_apps_dialog.py` - the dialog for setting, what user data of the Flatpak apps will be included in the configuration archive
- `install_flatpak_from_script.py` - installing Flatpak apps from the list to the system and copying user data from the configuration archive to the ~/.var/app directory
- `localization.py` - Based on the detected system language, the application sets the interface language (if the system language is not in the list of available languages, English is set), also sets the cache and application data folders and also the application version and release notes
- `main_window.py` - the GUI of the app
- `network_sharing.py` - synchronization between computers in the network within Python HTTP server or cloud drive folder
- `open_wiki.py` - opening the Github wiki of this app in the system language (if it is not available in the list of available languages, English opens)
- `periodic_saving.py` - saving configuration periodically
- `shortcuts_window.py` - showing available Keyboard shortcuts in the window
- `tty_environments.py` - detecting desktop environemnt in the TTY mode
