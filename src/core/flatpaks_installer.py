#!/usr/bin/env python3
import os, subprocess, shutil, json, time
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
        print("[COPY] Copying the Flatpak's user data to ~/.var/app", flush=True)
        if os.path.exists(f"app"):
            os.system(f"cp -au ./app/ ~/.var/")

        archive_file = "Flatpak_Apps/flatpak-apps-data.tgz" if os.path.exists("Flatpak_Apps/flatpak-apps-data.tgz") else "flatpak-apps-data.tgz"

        if os.path.exists(archive_file):
            tar_cmd = ["tar", "-xzf", archive_file, "-C", f"{Path.home()}/.var"]
            for d_app in disabled_flatpaks:
                tar_cmd.extend([f"--exclude={d_app}", f"--exclude=app/{d_app}"])
            subprocess.run(tar_cmd)
        print("✔ Copied Flatpak's user data", flush=True)

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
                    # Read all lines into memory
                    lines = f.readlines()

                # The file is safely closed here, we process the list in memory
                for line in lines:
                    if 'flatpak' in line and 'install' in line:
                        parts = line.split()

                        app_id = None
                        for part in parts:
                            # Look for something that looks like an app ID (e.g. com.obsproject.Studio)
                            if "." in part and not part.startswith("-"):
                                app_id = part
                                break

                        if not app_id:
                            continue

                        if app_id in disabled_flatpaks:
                            print(f"[SKIP] Disabled app: {app_id}", flush=True)
                            continue

                        # Determine if it's a user or system install
                        method = "--user" if "--user" in parts else "--system"
                        desired_flatpaks[app_id] = method

        # Count the actual valid apps we found, not just raw lines in the file
        apps_count = len(desired_flatpaks)
        if not desired_flatpaks:
            print("Installation queue is empty.", flush=True)
        else:
            print(f"Installing {apps_count} apps", flush=True)

        # Get currently installed Flatpaks first, before doing any math
        system_flatpak_dir = '/var/lib/flatpak/app'
        user_flatpak_dir = os.path.expanduser('~/.local/share/flatpak/app')
        installed_apps = {}

        for directory, method in [(system_flatpak_dir, '--system'), (user_flatpak_dir, '--user')]:
            if os.path.exists(directory):
                for app in os.listdir(directory):
                    if os.path.isdir(os.path.join(directory, app)):
                        installed_apps[app] = method

        # Filter out the apps that are already on the system
        apps_to_install = {app: method for app, method in desired_flatpaks.items() if app not in installed_apps}
        apps_count = len(apps_to_install)

        # Print the ones we are skipping just so the user knows
        for app in desired_flatpaks:
            if app in installed_apps:
                print(f"[INFO] {app} is already available in the system.", flush=True)

        # Now handle the actual installation queue
        if apps_count == 0:
            print("Installation queue is empty. Nothing new to install.", flush=True)
        else:
            print(f"Installing {apps_count} new apps", flush=True)

            # Start the installation loop only for the missing apps
            for i, (app, method) in enumerate(apps_to_install.items(), start=1):
                print(f"↓ Installing {app} ({i}/{apps_count})", flush=True)

                # Ensure the user repo exists if we are doing a user install
                if method == '--user':
                    os.system("flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo")

                # Run the actual Flatpak install command
                subprocess.run(['flatpak', 'install', method, 'flathub', app, '-y'])

        print("✔ All apps have been installed", flush=True)

    # Remove Flatpaks, which are not in the list (only if it's allowed by the user)
    if not keep_flatpaks:
        for app, method in installed_apps.items():
            if app not in desired_flatpaks:
                print(f"[REMOVE] {method.title()} Flatpak: {app}", flush=True)
                subprocess.run(['flatpak', 'uninstall', method, app, '--delete-data', '-y'])

        # Remove orphaned ~/.var/app directories
        user_var_app = Path.home() / ".var/app"
        if user_var_app.exists():
            for app_dir in user_var_app.iterdir():
                if app_dir.is_dir() and app_dir.name not in desired_flatpaks:
                    print(f"[REMOVE] Orphaned Flatpak user data: {app_dir.name}", flush=True)
                    shutil.rmtree(app_dir)
        print("[OK] All useless apps have been removed", flush=True)

    print("✔ All operations have been completed successfully.")

else:
    print("Nothing to do.", flush=True)

# Remove the autostart file after finishing the operations
autostart_file = f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"
if os.path.exists(autostart_file):
    os.remove(autostart_file)
