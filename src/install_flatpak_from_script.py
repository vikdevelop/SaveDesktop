#!/usr/bin/python3
import os
from pathlib import Path

DATA_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"
DATA_NATIVE = f"{Path.home()}/.local/share/io.github.vikdevelop.SaveDesktop"

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

os.system(f"cp -R {DATA_FLATPAK}/user {Path.home()}/.config/dconf/ && cp -R {DATA_FLATPAK}/user {Path.home()}/.config/dconf/")
os.system(f"cp -R {DATA_NATIVE}/user {Path.home()}/.config/dconf/ && cp -R {DATA_NATIVE}/user {Path.home()}/.config/dconf/")

# Install Flatpak apps from list
if os.path.exists(f"{DATA_FLATPAK}/installed_flatpaks.sh"):
    os.system(f"sh {DATA_FLATPAK}/installed_flatpaks.sh")
    os.system(f"rm {DATA_FLATPAK}/installed_flatpaks.sh")
elif os.path.exists(f"{DATA_NATIVE}/installed_flatpaks.sh"):
    os.system(f"sh {DATA_NATIVE}/installed_flatpaks.sh")
    os.system(f"rm {DATA_NATIVE}/installed_flatpaks.sh")
else:
    print("List with installed Flatpak apps is not exists.")
