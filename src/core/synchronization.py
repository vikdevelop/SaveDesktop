#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, date, timedelta
import subprocess, os, locale, json, sys, gi, socket, shutil, zipfile, tarfile, re
from gi.repository import Gio, GLib
from savedesktop.globals import *
from savedesktop.core.password_store import PasswordStore
from savedesktop.gui.password_checker import PasswordCheckerApp

dt = datetime.now()

class Syncing:
    def __init__(self):
        self.last_sync_date = self.load_last_sync_date()
        if not settings["file-for-syncing"]:
            print("Synchronization is not set up.")
        else:
            self.get_sync_interval()
    
    # Load the last date from the {DATA}/sync-info.json file
    def load_last_sync_date(self):
        sync_file = f"{DATA}/sync-info.json"
        if os.path.exists(sync_file):
            with open(sync_file) as s:
                jl = json.load(s)
            return date.fromisoformat(jl.get("last-synced", "2000-01-01"))
        return date(2000, 1, 1)
    
    # Get the sync interval from the settings["periodic-import"] string
    def get_sync_interval(self):
        intervals = {
            "Never2": None,
            "Daily2": 1,
            "Weekly2": 7,
            "Monthly2": 30,
        }
        interval = intervals.get(settings["periodic-import"], None)
        if interval is None:
            print("Synchronization is not set up. Maybe you have selected the Never interval?")
        else:
            self.check_and_sync(interval)
    
    # Check, if the synchronization is necessary for that day
    def check_and_sync(self, interval):
        today = date.today()
        if (today - self.last_sync_date).days >= interval:
            self.download_config()
        else:
            print(f"Sync not needed today. Last sync was on {self.last_sync_date}.")
    
    # Download the configuration archive from the cloud drive folder
    def download_config(self):
        print("MODE: Synchronization")
        self._send_notification_at_startup()
        if not os.path.exists(f"{settings['file-for-syncing']}/SaveDesktop.json"):
            err_str = _("An error occurred")
            err = "SaveDesktop.json: directory or file does not exist."
            os.system(f'notify-send "{err_str}" "{err}"')
        else:
            self.get_pb_info()
            self.create_status_file()
            self.get_zip_file_status()

    # Send a notification about the started synchronization
    def _send_notification_at_startup(self):
        orig_str = _("<big><b>Importing configuration …</b></big>\nImporting configuration from:\n<i>{}</i>\n")
        status_str = orig_str
        subtitle = (
            status_str
            .replace("<big>", "")
            .replace("</big>", "")
            .replace("<b>", "")
            .replace("</b>", "")
            .replace("<i>", "")
            .replace("</i>", "")
            .split("…", 1)[-1].strip()
        ).format(f'{settings["file-for-syncing"]}/{settings["filename-format"]}.sd.zip')
        os.system(f'notify-send "Save Desktop Synchronization" "{subtitle}"')
        
    # Get data from the SaveDesktop.json file such as filename format, periodic saving interval and folder (for bidirectional synchronization)
    def get_pb_info(self):
        with open(os.path.join(settings['file-for-syncing'], "SaveDesktop.json")) as data:
            info = json.load(data)
        self.file = info["filename"].replace(" ", "_") if " " in info["filename"] else info["filename"]
        if settings["bidirectional-sync"]:
            settings["filename-format"] = info["filename"]
            settings["periodic-saving"] = info["periodic-saving-interval"]
            settings["periodic-saving-folder"] = settings["file-for-syncing"]
        
    # Check, if the ZIP archive is encrypted or not
    def get_zip_file_status(self):
        try:
            status = any(z.flag_bits & 0x1 for z in zipfile.ZipFile(f"{settings['file-for-syncing']}/{self.file}.sd.zip").infolist() if not z.filename.endswith("/"))
        except:
            status = False

        if status == True:
            self.get_pwd_from_file()
        else:
            self.password = None
            self.call_archive_command()
    
    # Get a password from the {DATA}/password file
    def get_pwd_from_file(self):
        def try_passwordstore():
            try:
                p = PasswordStore()
                return p.password
            except Exception as e:
                print(f"[PasswordStore failed] {e}")
                return None

        # #1 First attempt
        self.password = try_passwordstore()

        # #2 If it fails, run GUI
        if not self.password:
            app = PasswordCheckerApp()
            app.run([])
            self.password = try_passwordstore()

        # #3 If password is still unavailable, get it from the {CACHE}/temp_file
        if not self.password and os.path.exists(f"{CACHE}/temp_file"):
            with open(f"{CACHE}/temp_file") as ep:
                self.password = ep.read().strip()

        # #4 Final check
        if not self.password:
            msg = _("Password not entered, or it's incorrect. Unable to continue.")
            err_occurred = _("An error occurred")
            os.system(f'notify-send "{err_occurred}" "{msg}"')
        else:
            # #5 Continue in extraction
            print("Password retrieved from file successfully")
            self.call_archive_command()

    # Create this file to enable some synchronization features in terms of encryption in archive.py
    def create_status_file(self):
        open(f"{CACHE}/sync", "w").close()
                
    # Extract the configuration archive
    def call_archive_command(self):
        self.archive_mode = "--unpack"
        self.archive_name = f"{settings['file-for-syncing']}/{self.file}.sd.zip"

        subprocess.run([sys.executable, "-m", "savedesktop.core.archive", self.archive_mode, self.archive_name], env={**os.environ, "PYTHONPATH": f"{app_prefix}"})
        if os.path.exists(f"{CACHE}/sync"):
            self.done()
    
    def done(self):
        with open(f"{DATA}/sync-info.json", "w") as s:
            json.dump({"last-synced": date.today().isoformat()}, s)
        
        # Send a notification about finished synchronization
        os.system(f"notify-send 'Save Desktop Synchronization ({self.file})' '{_('The configuration has been applied!')} {_('Changes will only take effect after the next login')}' -i io.github.vikdevelop.SaveDesktop-symbolic")

        # Remove this status file after finished operations
        if os.path.exists(f"{CACHE}/sync"):
            os.remove(f"{CACHE}/sync")

Syncing()
