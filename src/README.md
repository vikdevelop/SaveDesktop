# Navigation
In this directory is located the most important part of the app, which is its source code.
Because there are a lot of files, this README helps you with navigate in this directory.

Individual scripts take care of:
- `config.py` - saving and importing user configuration from and in the configuration archive
- `install_flatpak_from_script.py` - installing Flatpak apps from the list to the system and copying user data from the configuration archive to the ~/.var/app directory
- `items_dialog.py` - selecting what items should be included in the configuration archive
- `localization.py` - setting the app's language, cache and data directories and more
- `main_window.py` - the GUI of the app
- `open_wiki.py` - opening the Github wiki pages of this app in the system language (if it is not available in the list of available languages, English opens)
- `periodic_saving.py` - saving configuration periodically
- `shortcuts_window.py` - showing available Keyboard shortcuts in the window
- `synchronization.py` - syncing between computers in the network within Python HTTP server or cloud drive folder
