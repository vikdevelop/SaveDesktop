#!/usr/bin/env python3
import os, subprocess, sys, shutil
from pathlib import Path

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
if os.path.exists(f"{CACHE_FLATPAK}/workspace"):
    dest_dir = f"{CACHE_FLATPAK}/workspace"
else:
    dest_dir = None
   
# If the destination directory variable is not 'None', continue in installing Flatpak apps
if dest_dir:
    # If the destination directory has a directory with installed Flatpak apps user data, install them
    if os.path.exists(f"{dest_dir}/app"):
        print("copying the Flatpak apps' user data to the ~/.var/app directory")
        os.system(f"cp -au {dest_dir}/app/ ~/.var/")
    
    # If the flatpak-apps-data.tgz archive exists, unpack it to the ~/.var/app directory
    if os.path.exists(f"{dest_dir}/flatpak-apps-data.tgz"):
        subprocess.run(["tar", "-xzvf", "flatpak-apps-data.tgz", "-C", f"{Path.home()}/.var"])

    # If the Bash scripts for installing Flatpak apps to the system exist, install them
    if os.path.exists(f"{dest_dir}/installed_flatpaks.sh") or os.path.exists(f"{dest_dir}/installed_user_flatpaks.sh"):
        print("installing the Flatpak apps on the system")

        # If the Flathub repository in user installation doesn't exist, add it
        if os.path.getsize(f"{dest_dir}/installed_user_flatpaks.sh") > 5:
            os.system("flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo")
        # Install Flatpak apps from list
        installed_flatpaks_files = [f'{dest_dir}/installed_flatpaks.sh', f'{dest_dir}/installed_user_flatpaks.sh']
        system_flatpak_dir = '/var/lib/flatpak/app'
        user_flatpak_dir = os.path.expanduser('~/.local/share/flatpak/app')
        # Load Flatpaks from bash scripts
        installed_flatpaks = {}
        for file in installed_flatpaks_files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    for line in f:
                        if line.startswith('flatpak install'):
                            parts = line.split()
                            if '--user' in parts:
                                app = parts[3]
                                installed_flatpaks[app] = '--user'
                            elif '--system' in parts:
                                app = parts[3]
                                installed_flatpaks[app] = '--system'

        # Get installed Flatpaks in the specified directories
        installed_apps = set()
        for directory in [system_flatpak_dir, user_flatpak_dir]:
            if os.path.exists(directory):
                installed_apps.update(app for app in os.listdir(directory) if os.path.isdir(os.path.join(directory, app)))

        # Compare Flatpaks listed in the Bash scripts with the installed ones
        flatpaks_to_install = {app: method for app, method in installed_flatpaks.items() if app not in installed_apps}

        if flatpaks_to_install:
            for app, method in flatpaks_to_install.items():
                subprocess.run(['flatpak', 'install', method, 'flathub', app, '-y'])
        else:
            print('All Flatpak apps are installed.')
else:
    print("Nothing to do.")

# Remove the autostart file after finishing the operations
autostart_file = f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"
if os.path.exists(autostart_file):
    os.remove(autostart_file)

# Remove the cache dir after finishing the operations
shutil.rmtree(f"{CACHE_FLATPAK}/workspace")
