#!/usr/bin/python3
import os
from pathlib import Path
import subprocess

CACHE_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"

# Check Desktop Environment
desktop_env = os.getenv("XDG_CURRENT_DESKTOP")
if desktop_env in ['GNOME', 'ubuntu:GNOME', 'zorin:GNOME']:
    environment = 'GNOME'
else:
    environment = None

# Activate gsettings property
if environment:
    if not subprocess.getoutput("gsettings get org.gnome.shell disable-user-extensions") == "false":
        os.system("gsettings set org.gnome.shell disable-user-extensions false")
    
# Check if the required directories exist in the cache directory
if os.path.exists(f"{CACHE_FLATPAK}/import_config"):
    dest_dir = f"{CACHE_FLATPAK}/import_config"
elif os.path.exists(f"{CACHE_FLATPAK}/syncing"):
    dest_dir = f"{CACHE_FLATPAK}/syncing"
else:
    dest_dir = None
   
# If the destination directory variable is not 'None', continue in installing Flatpak apps
if not dest_dir == None:
    # If the destination directory has a directory with installed Flatpak apps user data, install them
    if os.path.exists(f"{dest_dir}/app"):
        print("copying the Flatpak apps' user data to the ~/.var/app directory")
        os.system(f"cp -au {dest_dir}/app/ ~/.var/")
    
    # If the Bash scripts for installing Flatpak apps to the system, install them
    if os.path.exists(f"{dest_dir}/installed_flatpaks.sh") or os.path.exists(f"{dest_dir}/installed_user_flatpaks.sh"):
        print("installing the Flatpak apps on the system")
        # Install Flatpak apps from list
        installed_flatpaks_files = [f'{dest_dir}/installed_flatpaks.sh', f'{dest_dir}/installed_user_flatpaks.sh']
        system_flatpak_dir = '/var/lib/flatpak/app'
        user_flatpak_dir = os.path.expanduser('~/.local/share/flatpak/app')
        # Load Flatpaks from bash scripts
        installed_flatpaks = set()
        for file in installed_flatpaks_files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    installed_flatpaks.update(line.split()[3] for line in f if line.startswith('flatpak install'))

        # Get installed Flatpaks in the specified directories
        installed_apps = set()
        for directory in [system_flatpak_dir, user_flatpak_dir]:
            if os.path.exists(directory):
                installed_apps.update(app for app in os.listdir(directory) if os.path.isdir(os.path.join(directory, app)))

        # Compare Flatpaks listed in the Bash scripts with the installed ones
        flatpaks_to_install = installed_flatpaks - installed_apps

        if flatpaks_to_install:
            for app in flatpaks_to_install:
                subprocess.run(['flatpak', 'install', '--user', 'flathub', app, '-y'])
        else:
            print('All Flatpak apps are installed.')
        
    os.system(f'rm -rf {CACHE_FLATPAK}/*') # Remove the cache directory after the installing Flatpak apps (and optionally their data) are finished
else:
    print("Nothing to do.")
