#!/usr/bin/env python3
import os, subprocess, shutil, json
from pathlib import Path

CACHE_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp/workspace"

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
if os.path.exists(CACHE_FLATPAK):
    dest_dir = CACHE_FLATPAK
else:
    dest_dir = None
   
if dest_dir:
    os.chdir(dest_dir)
    # Check Flatpak user preferences
    with open(f"flatpak-prefs.json") as fl:
        j = json.load(fl)

    copy_data = j["copy-data"]
    install_flatpaks = j["install-flatpaks"]
    disabled_flatpaks = j["disabled-flatpaks"]
    keep_flatpaks = j["keep-flatpaks"]

    # Restore Flatpak user data archive
    if copy_data:
        if os.path.exists(f"app"):
            print("copying the Flatpak apps' user data to the ~/.var/app directory")
            os.system(f"cp -au ./app/ ~/.var/")

        archive_file = "Flatpak_Apps/flatpak-apps-data.tgz" if os.path.exists("Flatpak_Apps/flatpak-apps-data.tgz") else "flatpak-apps-data.tgz"

        if os.path.exists(archive_file):
            tar_cmd = ["tar", "-xzvf", archive_file, "-C", f"{Path.home()}/.var"]
            for d_app in disabled_flatpaks:
                tar_cmd.extend([f"--exclude={d_app}", f"--exclude=app/{d_app}"])
            subprocess.run(tar_cmd)

    # Load Flatpaks from bash scripts
    if install_flatpaks:
        if os.path.exists("Flatpak_Apps"):
            installed_flatpaks_files = ['Flatpak_Apps/installed_flatpaks.sh', 'Flatpak_Apps/installed_user_flatpaks.sh']
        else:
            installed_flatpaks_files = ['installed_flatpaks.sh', 'installed_user_flatpaks.sh']
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

                            # TADY JE TEN FIX PRO INSTALACI:
                            # Zkontrolujeme, jestli app_id není v blacklistu z flatpak-prefs.json
                            if app_id in disabled_flatpaks:
                                print(f"[SKIP] Přeskakuji instalaci a data zakázané appky: {app_id}")
                                continue

                            method = "--user" if "--user" in parts else "--system"
                            desired_flatpaks[app_id] = method

    # Remove Flatpaks, which are not in the list (only if it's allowed by the user)
    if not keep_flatpaks:
        for app, method in installed_apps.items():
            if app not in desired_flatpaks:
                print(f"[REMOVE] {method.title()} Flatpak: {app}")
                subprocess.run(['flatpak', 'uninstall', method, app, '--delete-data', '-y'])

        # Remove orphaned ~/.var/app directories
        user_var_app = Path.home() / ".var/app"
        if user_var_app.exists():
            for app_dir in user_var_app.iterdir():
                if app_dir.is_dir() and app_dir.name not in desired_flatpaks:
                    print(f"[REMOVE] Orphaned Flatpak user data: {app_dir.name}")
                    shutil.rmtree(app_dir)

else:
    print("Nothing to do.")

# Remove the autostart file after finishing the operations
autostart_file = f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"
if os.path.exists(autostart_file):
    os.remove(autostart_file)

# Remove the cache dir after finishing the operations
if os.path.exists(CACHE_FLATPAK):
    shutil.rmtree(CACHE_FLATPAK)
