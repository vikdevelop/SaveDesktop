from datetime import datetime
from datetime import date
from pathlib import Path
import json
import os
import gi
from gi.repository import GLib, Gio
from localization import _, CACHE, DATA, home, system_dir

# get current datetime
dt = datetime.now()
# get day
current_day = datetime.today()
# get first day of month
first_day = current_day.replace(day=1)

download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)

class PeriodicBackups:
    def __init__(self):
        self.settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
        
        # Get directory for storing periodic backups
        if self.settings["periodic-saving-folder"] == '':
            self.pbfolder = f'{download_dir}/SaveDesktop/archives'
        else:
            self.pbfolder = f'{self.settings["periodic-saving-folder"]}'
            
        if os.path.exists(f"{DATA}/periodic-saving.json"):
            with open(f"{DATA}/periodic-saving.json") as pb:
                jp = json.load(pb)
            if jp["saving-date"] == f'{date.today()}':
                print("The configuration has already been saved today.")
                exit()
            else:
                self.get_interval()
        else:
            self.get_interval()
        
    def get_interval(self):
        # Get periodic saving interval selected by the user
        if self.settings["periodic-saving"] == 'Never':
            print("Periodic saving are not set up.")
            exit()
        elif self.settings["periodic-saving"] == 'Daily':
            self.daily()
        elif self.settings["periodic-saving"] == 'Weekly':
            self.weekly()
        elif self.settings["periodic-saving"] == 'Monthly':
            self.monthly()
         
    # Periodic backups: daily
    def daily(self):
        self.backup()
        
    # Periodic backups: weekly
    def weekly(self):
        if date.today().weekday() == 0:
            self.backup()
        else:
            print("Today is not Monday.")
            
    # Periodic backups: monthly
    def monthly(self):
        if dt.day == 1:
            self.backup()
        else:
            print("Today is not first day of month.")
    
    # Create backup
    def backup(self):
        if self.pbfolder == f'{download_dir}/SaveDesktop/archives':
            try:
                if not os.path.exists(f"{download_dir}/SaveDesktop/archives"):
                    os.makedirs(f"{download_dir}/SaveDesktop/archives")
            except:
                os.system(f"mkdir {home}/Downloads")
                os.system(f"xdg-user-dirs-update --set DOWNLOAD {home}/Downloads")
                os.makedirs(f"{download_dir}/SaveDesktop/archives")
        if not os.path.exists(f"{CACHE}/periodic_saving"):
            os.mkdir(f"{CACHE}/periodic_saving")
        if " " in self.settings["filename-format"]:
            old_filename = f'{self.settings["filename-format"]}'
            filename = old_filename.replace(" ", "_")
        else:
            filename = self.settings["filename-format"]
        if self.settings["save-flatpak-data"] == True:
            with open(f"{CACHE}/.periodicfile.json", "w") as p:
                p.write('{\n "recent_file": "%s/%s.fd.sd.tar.gz"\n}' % (self.pbfolder, filename))
        else:
            with open(f"{CACHE}/.periodicfile.json", "w") as p:
                p.write('{\n "recent_file": "%s/%s.sd.tar.gz"\n}' % (self.pbfolder, filename))
        os.chdir(f"{CACHE}/periodic_saving")
        os.system(f"python3 {system_dir}/config.py --save")
        os.system(f"rm {CACHE}/.periodicfile.json")
        self.config_saved()
      
    # Message about saved config
    def config_saved(self):
        os.system(f"rm -rf {CACHE}/periodic-saving/*")
        with open(f"{DATA}/periodic-saving.json", "w") as pb:
            pb.write('{\n "saving-date": "%s"\n}' % date.today())
        print("Configuration saved.")
        exit()
    
PeriodicBackups()
