#!/usr/bin/python3
from pathlib import Path
from datetime import datetime
from datetime import date
from localization import _, CACHE, DATA, system_dir, home, settings
import subprocess
import os
import locale
import json
import gi
import socket
import shutil
import filecmp
import tarfile
from gi.repository import Gio, GLib

dt = datetime.now()

class Syncing:
    def __init__(self):
        # Check if user has same or empty IP address property
        if not settings["file-for-syncing"]:
            settings["manually-sync"] = False
            print("Synchronization is not set up.")
        elif not settings["bidirectional-sync"]:
            settings["manually-sync"] = False
            print("The bidirectional synchronization is turned off.")
        else:
            self.get_file_info()

    # Get info about synchronization
    def get_file_info(self):
        # Check if syncing directory exists
        if not os.path.exists(f"{CACHE}/syncing"):
            os.mkdir(f"{CACHE}/syncing")
        os.chdir(f"{CACHE}/syncing")
        if settings["periodic-import"] == "Never2":
            self.create_backup = False
            settings["manually-sync"] = False
            print("Synchronization is not set up.")
        elif settings["periodic-import"] == "Daily2":
            self.create_backup = True
            settings["manually-sync"] = False
            self.check_sync()
        elif settings["periodic-import"] == "Weekly2":
            self.create_backup = False
            settings["manually-sync"] = False
            if date.today().weekday() == 1:
                self.check_sync()
            else:
                print("Today is not Tuesday.")
        elif settings["periodic-import"] == "Monthly2":
            self.create_backup = False
            settings["manually-sync"] = False
            if dt.day == 2:
                self.check_sync()
            else:
                print("Today is not second day of month.")
        elif settings["periodic-import"] == "Manually2":
            self.create_backup = False
            settings["manually-sync"] = True
            self.check_sync()

    # Check if whether the synchronization has already taken place on this day
    def check_sync(self):
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
       if not settings['file-for-syncing'] == "" and not "sd.tar.gz" in settings["file-for-syncing"]:
            if os.path.exists(f'{settings["file-for-syncing"]}/SaveDesktop.json'):
                self.get_pb_info()
            else:
                subprocess.run(['python3', f'{system_dir}/periodic_saving.py', '--now'], check=True)
                self.get_pb_info()
            print("extracting the archive")
            try:
                with tarfile.open(f"{settings['file-for-syncing']}/{self.file}.sd.tar.gz", 'r:gz') as tar:
                    for member in tar.getmembers():
                        try:
                            tar.extract(member)
                        except PermissionError as e:
                            print(f"Permission denied for {member.name}: {e}")
            except Exception as e:
                os.system(f"notify-send 'An error occured' '{e}' -i io.github.vikdevelop.SaveDesktop-symbolic")
                exit()
            self.import_config()
       else:
            os.system("notify-send 'SaveDesktop' 'You have not set up the synchronization correctly. Please set it up in the app again.'")
            exit()
    
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
            if not settings["file-for-syncing"]:
                if not os.path.exists(info["periodic-saving-folder"]) and "gvfs" in info["periodic-saving-folder"]:
                    uid = os.getuid() # get user ID
                    periodic_saving_folder = re.sub(r'user/\d+/', f'user/{uid}/', periodic_saving_folder)
                else:
                    periodic_saving_folder = info["periodic-saving-folder"]
                settings["file-for-syncing"] = periodic_saving_folder
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
        if not os.path.exists(f"{CACHE}/syncing/copying_flatpak_data"):
            os.system(f"rm -rf {CACHE}/syncing/*")
        [os.remove(path) for path in [f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.MountDrive.desktop"] if os.path.exists(path)]
        print("Configuration has been synced successfully.")
        os.system(f"notify-send 'SaveDesktop ({self.file})' '{_['config_imported']} {_['periodic_saving_desc']}' -i io.github.vikdevelop.SaveDesktop-symbolic")

Syncing()
