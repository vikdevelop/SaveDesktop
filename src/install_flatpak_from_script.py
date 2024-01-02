#!/usr/bin/python3
import os
from pathlib import Path

DATA_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"
CACHE_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"

# Check Desktop Environment
if os.getenv("XDG_CURRENT_DESKTOP") == 'GNOME':
    environment = 'GNOME'
elif os.getenv("XDG_CURRENT_DESKTOP") == 'ubuntu:GNOME':
    environment = 'GNOME'
elif os.getenv("XDG_CURRENT_DESKTOP") == 'zorin:GNOME':
    environment = 'GNOME'
else:
    environment = 'None'

# Activate gsettings property
if environment == 'GNOME':
    os.system("gsettings set org.gnome.shell disable-user-extensions false")

if os.path.exists(f"{CACHE_FLATPAK}/import_config/app"):
    with open(f"{CACHE_FLATPAK}/copying_flatpak_data", "w") as f:
        f.write("copying flatpak data ...")
    os.system(f"cp -R {CACHE_FLATPAK}/import_config/app ~/.var/")
    os.system(f"rm -rf {CACHE_FLATPAK}/*")
else:
    print("A directory with user data for the installed Flatpak apps does not exist.")

# Install Flatpak apps from list
if os.path.exists(f"{DATA_FLATPAK}/installed_flatpaks.sh"):
    os.system(f"sh {DATA_FLATPAK}/installed_flatpaks.sh && sh {DATA_FLATPAK}/installed_user_flatpaks.sh")
    os.system(f"rm {DATA_FLATPAK}/*.sh")
else:
    print("A list of installed Flatpak apps does not exist.")
    
