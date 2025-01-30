#!/usr/bin/python3
from pathlib import Path
from datetime import datetime
from datetime import date
from localization import _, CACHE, DATA, system_dir, home, settings
import subprocess, os, locale, json, gi, socket, shutil, tarfile, re
from gi.repository import Gio, GLib

dt = datetime.now()

class Syncing:
    def __init__(self):
        # Check, if the user has filled out the file-for-syncing property
        if not settings["file-for-syncing"]:
            settings["manually-sync"] = False
            print("Synchronization is not set up.")
        else:
            self.get_sync_interval()

    # Get info about synchronization
    def get_sync_interval(self):
        if settings["periodic-import"] == "Never2":
            settings["manually-sync"] = False
            print("Synchronization is not set up.")
        elif settings["periodic-import"] == "Daily2":
            settings["manually-sync"] = False
            self.check_sync_date()
        elif settings["periodic-import"] == "Weekly2":
            settings["manually-sync"] = False
            if date.today().weekday() == 1:
                self.check_sync_date()
            else:
                print("Today is not Tuesday.")
        elif settings["periodic-import"] == "Monthly2":
            settings["manually-sync"] = False
            if dt.day == 2:
                self.check_sync_date()
            else:
                print("Today is not second day of month.")
        elif settings["periodic-import"] == "Manually2":
            settings["manually-sync"] = True
            self.check_sync_date()

    # Check if whether the synchronization has already taken place on this day
    def check_sync_date(self):
        if os.path.exists(f"{DATA}/sync-info.json"):
            with open(f"{DATA}/sync-info.json") as s:
                jl = json.load(s)
            if jl["sync-date"] == f'{date.today()}':
                print("The configuration has already been imported today.")
                exit()
            else:
                if settings["periodic-import"] == "Manually2":
                    if os.path.exists(f"{CACHE}/.from_app"):
                        self.download_config()
                    else:
                        print("Please sync from the SaveDesktop app")
                else:
                    self.download_config()
        else:
            if settings["periodic-import"] == "Manually2":
                if os.path.exists(f"{CACHE}/.from_app"):
                    self.download_config()
                else:
                    print("Please sync from the SaveDesktop app")
            else:
                self.download_config()
               
    # Download archive from URL
    def download_config(self):
        # send a notification about progressing synchronization
        subtitle = (lambda s: re.sub(r'<.*?>', '', s).split('…')[-1].strip())(_["importing_config_status"].format(settings["file-for-syncing"]))
        os.system(f'notify-send "SaveDesktop Synchronization" "{subtitle}"')
        
        # check, if the selected cloud drive folder contains the SaveDesktop.json file or not
        if os.path.exists(f'{settings["file-for-syncing"]}/SaveDesktop.json'):
            self.get_pb_info()
        else:
            subprocess.run(['python3', f'{system_dir}/periodic_saving.py', '--now'], check=True)
            self.get_pb_info()
        
        # Check if syncing directory exists
        os.makedirs(f"{CACHE}/syncing", exist_ok=True)
        os.chdir(f"{CACHE}/syncing")
        
        # create a txt file to prevent removing the progressing synchronization after closing the app window
        os.system("echo > sync_status")
        
        # extract the configuration archive
        print("extracting the archive")
        try:
            with tarfile.open(f"{settings['file-for-syncing']}/{self.file}.sd.tar.gz", 'r:gz') as tar:
                for member in tar.getmembers():
                    try:
                        tar.extract(member)
                    except PermissionError as e:
                        print(f"Permission denied for {member.name}: {e}")
        except Exception as e:
            os.system(f"notify-send '{_['err_occured']}' '{e}' -i io.github.vikdevelop.SaveDesktop-symbolic")
            exit()
        self.import_config()
    
    # Get info about selected periodic saving interval, periodic saving folder and filename from the {cloud_folder}/SaveDesktop.json
    def get_pb_info(self):
        with open(os.path.join(settings['file-for-syncing'], "SaveDesktop.json")) as data:
            info = json.load(data)
        
        # check if the filename has spaces or not
        if " " in info["filename"]:
            old_filename = info["filename"]
            self.file = old_filename.replace(" ", "_")
        else:
            self.file = info["filename"]
        
        # If bidirectional synchronization is enabled, set the periodic saving interval, folder, and filename format, and folder for synchronizaton from the SaveDesktop.json file
        if settings["bidirectional-sync"] == True:
            settings["filename-format"] = info["filename"]
            settings["periodic-saving"] = info["periodic-saving-interval"]
            settings["periodic-saving-folder"] = settings["file-for-syncing"]
        
    # Sync configuration
    def import_config(self):
        os.system(f"python3 {system_dir}/config.py --import_")
        self.done()

    # Message about finished synchronization
    def done(self):
        if not settings["manually-sync"] == True:
            with open(f"{DATA}/sync-info.json", "w") as s:
                s.write('{\n "sync-date": "%s"\n}' % date.today())
        os.system("rm sync_status") if all(not os.path.exists(app_path) for app_path in ["app", "installed_flatpaks.sh", "installed_user_flatpaks.sh"]) else None
        [os.remove(path) for path in [f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.MountDrive.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.server.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"] if os.path.exists(path)]
        print("Configuration has been synced successfully.")
        os.system(f"notify-send 'SaveDesktop ({self.file})' '{_['config_imported']} {_['periodic_saving_desc']}' -i io.github.vikdevelop.SaveDesktop-symbolic")

Syncing()
