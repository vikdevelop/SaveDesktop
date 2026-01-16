#!/usr/bin/env python3
import os, subprocess, shutil
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
   
if dest_dir:
    # Restore Flatpak user data archive if exists
    if os.path.exists(f"{dest_dir}/app"):
        print("copying the Flatpak apps' user data to the ~/.var/app directory")
        os.system(f"cp -au {dest_dir}/app/ ~/.var/")

    if os.path.exists(f"{dest_dir}/flatpak-apps-data.tgz"):
        subprocess.run(["tar", "-xzvf", "flatpak-apps-data.tgz", "-C", f"{Path.home()}/.var"])

    # Load Flatpaks from bash scripts
    installed_flatpaks_files = [f'{dest_dir}/installed_flatpaks.sh', f'{dest_dir}/installed_user_flatpaks.sh']
    desired_flatpaks = {}
    for file in installed_flatpaks_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('flatpak install'):
                        parts = line.split()
                        if len(parts) < 4:
                            continue
                        app_id = parts[3]
                        method = "--user" if "--user" in parts else "--system"
                        desired_flatpaks[app_id] = method

    # Get currently installed Flatpaks
    system_flatpak_dir = '/var/lib/flatpak/app'
    user_flatpak_dir = os.path.expanduser('~/.local/share/flatpak/app')
    installed_apps = {}
    for directory, method in [(system_flatpak_dir, '--system'), (user_flatpak_dir, '--user')]:
        if os.path.exists(directory):
            for app in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, app)):
                    installed_apps[app] = method

    # Remove Flatpaks, which are not in the list
    for app, method in installed_apps.items():
        if app not in desired_flatpaks:
            print(f"[REMOVE] {method.title()} Flatpak: {app}")
            subprocess.run(['flatpak', 'uninstall', method, app, '--delete-data', '-y'])

    for app, method in desired_flatpaks.items():
        if app not in installed_apps:
            print(f"[INSTALL] Installing {app} ({method})")
            if method == '--user':
                os.system("flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo")
            subprocess.run(['flatpak', 'install', method, 'flathub', app, '-y'])

else:
    print("Nothing to do.")

# Remove the autostart file after finishing the operations
autostart_file = f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"
if os.path.exists(autostart_file):
    os.remove(autostart_file)

# Remove the cache dir after finishing the operations
if os.path.exists(f"{CACHE_FLATPAK}/workspace"):
    shutil.rmtree(f"{CACHE_FLATPAK}/workspace")

