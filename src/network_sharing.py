#!/usr/bin/python3
from pathlib import Path
from datetime import datetime
from datetime import date
from localization import _, CACHE, DATA, IPAddr, system_dir, flatpak, snap, home
import subprocess
import os
import locale
import json
import gi
import socket
import shutil
import filecmp
from gi.repository import Gio, GLib

dt = datetime.now()

# Load GSettings database for show user app settings
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")

class Syncing:
    def __init__(self):
        # Check if user has same or empty IP address property
        if settings["url-for-syncing"] or settings["file-for-syncing"] == "":
            settings["manually-sync"] = False
            print("Synchronization is not set up.")
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
        if not settings['url-for-syncing'] == "":
            url = f"{settings['url-for-syncing']}"
            os.system(f"wget {url}")
            filename = url.split('/')[-1]
            self.file = filename.split('.')[0]
            if ".sd.tar.gz" in url:
                print("Downloading tar ...")
                if os.path.exists(f"{self.file}"):
                    os.system(f"tar -xf {self.file} ./")
                else:
                    os.system(f"tar -xf {self.file}.1 ./")
                self.import_config()
            else:
                os.system("notify-send 'SaveDesktop Synchronization' 'An error occurred while downloading the configuration archive. Please set up the synchronization in the app again.'")
                exit()
        elif not settings['file-for-syncing'] == "" and not "sd.tar.gz" in settings["file-for-syncing"]:
            filename = subprocess.getoutput(f"cat {settings['file-for-syncing']}/SaveDesktop-sync-file")
            try:
                tarfile.open(f"{settings['file-for-syncing']}/{filename}", 'r:gz').extractall()
            except Exception as e:
                os.system(f"notify-send 'An error occured' '{e}' -i io.github.vikdevelop.SaveDesktop-symbolic")
            self.file = filename
            self.import_config()
        else:
            os.system("notify-send 'SaveDesktop' 'You have not set up the synchronization correctly. Please set it up in the app again.'")
            exit()
            
    # Sync configuration
    def import_config(self):
        os.system(f"python3 {system_dir}/config.py --import_")
        self.done()

    # Message about done synchronization
    def done(self):
        if not settings["manually-sync"] == True:
            with open(f"{DATA}/sync-info.json", "w") as s:
                s.write('{\n "sync-date": "%s"\n}' % date.today())
        if not os.path.exists(f"{CACHE}/syncing/copying_flatpak_data"):
            os.system(f"rm -rf {CACHE}/syncing/*")
        print("Configuration has been synced successfully.")
        os.system(f"notify-send 'SaveDesktop ({self.file[:-10]})' '{_['config_imported']} {_['periodic_saving_desc']}' -i io.github.vikdevelop.SaveDesktop-symbolic")

Syncing()
