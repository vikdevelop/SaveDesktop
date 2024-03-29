#!/usr/bin/python3
import os
from pathlib import Path
import subprocess

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
    if not os.path.exists(f"{CACHE_FLATPAK}/import_config/copying_flatpak_data"):
        with open(f"{CACHE_FLATPAK}/copying_flatpak_data", "w") as f:
            f.write("copying flatpak data ...")
    os.system(f"cp -au {CACHE_FLATPAK}/import_config/app/ ~/.var/")
    os.system(f"rm -rf {CACHE_FLATPAK}/*")
elif os.path.exists(f"{CACHE_FLATPAK}/syncing/app"):
    if not os.path.exists(f"{CACHE_FLATPAK}/syncing/copying_flatpak_data"):
        with open(f"{CACHE_FLATPAK}/copying_flatpak_data", "w") as f:
            f.write("copying flatpak data ...")
    print("copying user data ...")
    os.system(f"cp -au {CACHE_FLATPAK}/syncing/app/ ~/.var/")
    os.system(f"rm -rf {CACHE_FLATPAK}/*")

# Install Flatpak apps from list
if os.path.exists(f"{DATA_FLATPAK}/installed_flatpaks.sh"):
    os.system(f"sh {DATA_FLATPAK}/installed_flatpaks.sh && sh {DATA_FLATPAK}/installed_user_flatpaks.sh")
    os.system(f"rm {DATA_FLATPAK}/*.sh")
else:
    print("List with installed Flatpak apps is not exists.")
    
