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
    if not subprocess.getoutput("gsettings get org.gnome.shell disable-user-extensions") == "false":
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
installed_flatpaks_files = [f'{DATA_FLATPAK}/installed_flatpaks.sh', f'{DATA_FLATPAK}/installed_user_flatpaks.sh']
system_flatpak_dir = '/var/lib/flatpak/app'
user_flatpak_dir = os.path.expanduser('~/.local/share/flatpak/app')

# load Flatpaks from bash scripts
installed_flatpaks = set()
for file in installed_flatpaks_files:
    if os.path.exists(file):
        with open(file, 'r') as f:
            for line in f:
                if line.startswith('flatpak install'):
                    installed_flatpaks.add(line.split()[3])

# get installed Flatpaks in the system and the home directories
installed_apps = set()
for directory in [system_flatpak_dir, user_flatpak_dir]:
    for app in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, app)):
            installed_apps.add(app)

# compare Flatpaks listed in the Bash scripts with the Flatpaks installed in the system
flatpaks_to_install = installed_flatpaks - installed_apps

if flatpaks_to_install:
    for app in flatpaks_to_install:
        subprocess.run(['flatpak', 'install', '--user', app, '-y'])
        os.system(f"rm -rf {DATA_FLATPAK}/*.sh")
else:
    print('All Flatpak apps are installed.')
