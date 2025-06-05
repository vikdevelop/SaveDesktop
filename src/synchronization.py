#!/usr/bin/python3
from pathlib import Path
from datetime import datetime, date, timedelta
import subprocess, os, locale, json, gi, socket, shutil, zipfile, tarfile, re
from gi.repository import Gio, GLib
from localization import *
from password_store import *

dt = datetime.now()

class Syncing:
    def __init__(self):
        self.last_sync_date = self.load_last_sync_date()
        if not settings["file-for-syncing"]:
            settings["manually-sync"] = False
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
            "Manually2": None
        }
        interval = intervals.get(settings["periodic-import"], None)
        if interval is None:
            settings["manually-sync"] = settings["periodic-import"] == "Manually2"
            if settings["manually-sync"]:
                self.check_sync_date()
            else:
                print("Synchronization is not set up.")
        else:
            settings["manually-sync"] = False
            self.check_and_sync(interval)
    
    # Check, if the synchronization is necessary for that day
    def check_and_sync(self, interval):
        today = date.today()
        if (today - self.last_sync_date).days >= interval:
            self.check_manually_sync_status()
        else:
            print(f"Sync not needed today. Last sync was on {self.last_sync_date}.")
    
    # Check, if "Manually" is the sync interval
    def check_manually_sync_status(self):
        if settings["periodic-import"] == "Manually2" and not os.path.exists(f"{CACHE}/.from_app"):
            print("Please sync from the SaveDesktop app")
        else:
            self.download_config()
    
    # Download the configuration archive from the cloud drive folder
    def download_config(self):
        subtitle = (lambda s: re.sub(r'<.*?>', '', s).split('…')[-1].strip())(_["importing_config_status"].format(settings["file-for-syncing"]))
        os.system(f'notify-send "SaveDesktop Synchronization" "{subtitle}"')
        if not os.path.exists(f'{settings["file-for-syncing"]}/SaveDesktop.json'):
            subprocess.run(['python3', f'{system_dir}/periodic_saving.py', '--now'], check=True)
        self.get_pb_info()
        self.file = "test_Sync"
        os.makedirs(f"{CACHE}/syncing", exist_ok=True) # create the subfolder in the cache directory
        os.chdir(f"{CACHE}/syncing")
        os.system("echo > sync_status") # create a txt file to prevent removing the sync's folder content after closing the app window
        print("extracting the archive")
        self.get_zip_file_status()
        
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
            self.extract_archive()
    
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
            os.system("python3 /app/password_check_gui.py")
            self.password = try_passwordstore()

        # #3 If password is still unavailable, get it from the {DATA}/entered-password.txt file
        if not self.password and os.path.exists(f"{DATA}/entered-password.txt"):
            with open(f"{DATA}/entered-password.txt") as ep:
                self.password = ep.read().strip()

        # #4 Final check
        if not self.password:
            print("[Error] Password not enterred. Unable to continue.")
            os.system('notify-send "SaveDesktop Synchronization" "Password not entered. Unable to continue."')
            exit()

        # #5 Continue in extraction
        self.extract_archive()
                
    # Extract the configuration archive
    def extract_archive(self):
        print("No errors with getting a password detected.")
        try:
            if os.path.exists(f"{settings['file-for-syncing']}/{self.file}.sd.zip"):
                with zipfile.ZipFile(f"{settings['file-for-syncing']}/{self.file}.sd.zip", "r") as zip_ar:
                    for member in zip_ar.namelist():
                        if self.password != None:
                            zip_ar.extract(member, path=f"{CACHE}/syncing", pwd=self.password.encode("utf-8"))
                        else:
                            zip_ar.extract(member, path=f"{CACHE}/syncing")
            else:
                with tarfile.open(f"{settings['file-for-syncing']}/{self.file}.sd.tar.gz", 'r:gz') as tar:
                    for member in tar.getmembers():
                        try:
                            tar.extract(member)
                        except PermissionError as e:
                            print(f"Permission denied for {member.name}: {e}")
            self.password = None
            os.system(f"rm {DATA}/entered-password.txt")
        except Exception as e:
            os.system(f"notify-send '{_['err_occured']}' '{e}' -i io.github.vikdevelop.SaveDesktop-symbolic")
            exit()
        self.import_config()
    
    # Start importing a configuration from the configuration archive
    def import_config(self):
        os.system(f"python3 {system_dir}/config.py --import_")
        self.done()
    
    # Send a notification about finished synchronization and write the last date of synchronization
    def done(self):
        if not settings["manually-sync"]:
            with open(f"{DATA}/sync-info.json", "w") as s:
                json.dump({"last-synced": date.today().isoformat()}, s)
        os.system("rm sync_status") if all(not os.path.exists(app_path) for app_path in ["app", "installed_flatpaks.sh", "installed_user_flatpaks.sh"]) else None
        print("Configuration has been synced successfully.")
        os.system(f"notify-send 'SaveDesktop ({self.file})' '{_['config_imported']} {_['periodic_saving_desc']}' -i io.github.vikdevelop.SaveDesktop-symbolic")

Syncing()
