# Navigation
In this directory is located the most important part of the app, which is its source code.
Because there are a lot of files, this README helps you navigate in this directory.

What are the individual scripts used for?
- `config.py` - saving and importing a user configuration from and to the home folder's directories
- `install_flatpak_from_script.py` - installing Flatpak apps from the list to the system and copying user data from the configuration archive to the ~/.var/app directory
- `items_dialog.py` - selecting what items should be included in the configuration archive
- `localization.py` - setting up the app's language, cache, data directories, and more
- `main_window.py` - showing a GUI of the app
- `periodic_saving.py` - saving a configuration periodically
- `shortcuts_window.py` - showing available keyboard shortcuts in the window
- `synchronization.py` - importing a configuration archive from the cloud storage folder
