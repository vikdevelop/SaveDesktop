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
    with open("flatpak-prefs.json") as fl:
        j = json.load(fl)

    copy_data = j["copy-data"]
    install_flatpaks = j["install-flatpaks"]
    disabled_flatpaks = j["disabled-flatpaks"]
    keep_flatpaks = j["keep-flatpaks"]

    # ==========================================
    # PHASE 1: PRE-CALCULATION (Math only, no actions)
    # ==========================================
    desired_flatpaks = {}
    if install_flatpaks:
        files_to_check = ['Flatpak_Apps/installed_flatpaks.sh', 'Flatpak_Apps/installed_user_flatpaks.sh'] if os.path.exists("Flatpak_Apps") else ['installed_flatpaks.sh', 'installed_user_flatpaks.sh']
        for file in files_to_check:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    for line in f.readlines():
                        if 'flatpak' in line and 'install' in line:
                            parts = line.split()
                            app_id = next((p for p in parts if "." in p and not p.startswith("-")), None)
                            if app_id and app_id not in disabled_flatpaks:
                                desired_flatpaks[app_id] = "--user" if "--user" in parts else "--system"

    installed_apps = {}
    for directory, method in [('/var/lib/flatpak/app', '--system'), (os.path.expanduser('~/.local/share/flatpak/app'), '--user')]:
        if os.path.exists(directory):
            for app in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, app)):
                    installed_apps[app] = method

    apps_to_install = {app: method for app, method in desired_flatpaks.items() if app not in installed_apps}
    apps_to_remove = {app: method for app, method in installed_apps.items() if app not in desired_flatpaks} if not keep_flatpaks else {}

    # Calculate exact total steps
    total_steps = 0
    if copy_data: total_steps += 1
    if install_flatpaks: total_steps += len(apps_to_install)
    if not keep_flatpaks:
        total_steps += len(apps_to_remove)
        total_steps += 1 # 1 extra step for orphaned dir cleanup

    current_step = 0

    def report_progress():
        """Helper to print the hidden progress tag for the GTK UI"""
        global current_step
        current_step += 1
        print(f"[PROGRESS] {current_step}/{total_steps}", flush=True)

    if total_steps == 0:
        print("There's no need to install any new apps, since they're all available on your system.", flush=True)
    else:
        # ==========================================
        # PHASE 2: EXECUTION
        # ==========================================

        # 1. Restore Data
        if copy_data:
            print("[COPY] Copying the Flatpak's user data to ~/.var/app", flush=True)
            if os.path.exists("app"):
                os.system("cp -au ./app/ ~/.var/")
            archive_file = "Flatpak_Apps/flatpak-apps-data.tgz" if os.path.exists("Flatpak_Apps/flatpak-apps-data.tgz") else "flatpak-apps-data.tgz"
            if os.path.exists(archive_file):
                tar_cmd = ["tar", "-xzf", archive_file, "-C", f"{Path.home()}/.var"]
                for d_app in disabled_flatpaks:
                    tar_cmd.extend([f"--exclude={d_app}", f"--exclude=app/{d_app}"])
                subprocess.run(tar_cmd)
            print("✔ Copied Flatpak's user data", flush=True)
            report_progress() # <--- SEND UPDATE TO UI

        # 2. Install Apps
        if install_flatpaks:
            for app in desired_flatpaks:
                if app in installed_apps:
                    print(f"[INFO] {app} is already available in the system.", flush=True)

            if apps_to_install:
                print(f"Installing {len(apps_to_install)} new apps", flush=True)
                for i, (app, method) in enumerate(apps_to_install.items(), start=1):
                    print(f"↓ Installing {app} ({i}/{len(apps_to_install)})", flush=True)
                    if method == '--user':
                        os.system("flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo")
                    subprocess.run(['flatpak', 'install', method, 'flathub', app, '-y'])
                    print(f"✔ Finished installing {app}", flush=True)
                    report_progress() # <--- SEND UPDATE TO UI

        # 3. Remove Apps & Cleanup
        if not keep_flatpaks:
            for app, method in apps_to_remove.items():
                print(f"[REMOVE] {method.title()} Flatpak: {app}", flush=True)
                subprocess.run(['flatpak', 'uninstall', method, app, '--delete-data', '-y'])
                report_progress() # <--- SEND UPDATE TO UI

            print("[REMOVE] Cleaning up orphaned user data...", flush=True)
            user_var_app = Path.home() / ".var/app"
            if user_var_app.exists():
                for app_dir in user_var_app.iterdir():
                    if app_dir.is_dir() and app_dir.name not in desired_flatpaks:
                        print(f"  -> Deleted: {app_dir.name}", flush=True)
                        shutil.rmtree(app_dir)
            print("[OK] All useless apps and orphaned data have been removed", flush=True)
            report_progress() # <--- SEND UPDATE TO UI

        print("✔ All operations have been completed successfully.", flush=True)

else:
    print("There's no need to install any new apps, since they're all available on your system.", flush=True)

# Remove the autostart file after finishing the operations
autostart_file = f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"
if os.path.exists(autostart_file):
    os.remove(autostart_file)
