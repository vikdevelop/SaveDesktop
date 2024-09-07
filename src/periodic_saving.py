import argparse, json, os, gi
from datetime import datetime
from datetime import date
from pathlib import Path
from gi.repository import GLib, Gio
from localization import _, CACHE, DATA, home, system_dir, settings

# Get the current date
dt = datetime.now()

# Get the current day
current_day = datetime.today()

# Get the first day of month
first_day = current_day.replace(day=1)

# Get the user downloads directory
download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)

class PeriodicBackups:
    def __init__(self):
        pass

    # Check, if the entered command has a --now argument or not
    def run(self, now: bool) -> None:
        # If the periodic saving value returns the default value, set the correct directory for the periodic saving file
        if settings["periodic-saving-folder"] == '':
            self.pbfolder = f'{download_dir}/SaveDesktop/archives'
        else:
            self.pbfolder = f'{settings["periodic-saving-folder"]}'

        if now:
            print("Saving immediately")
            self.backup()
        elif os.path.exists(f"{DATA}/periodic-saving.json"):
            with open(f"{DATA}/periodic-saving.json") as pb:
                jp = json.load(pb)
            if jp["saving-date"] == f'{date.today()}':
                print("The configuration has already been saved today.")
                exit()
            else:
                self.get_interval()
        else:
            self.get_interval()

    # Get selected periodic saving interval
    def get_interval(self):
        # Get periodic saving interval selected by the user
        if settings["periodic-saving"] == 'Never':
            print("Periodic saving is not set up.")
            exit()
        elif settings["periodic-saving"] == 'Daily':
            self.daily()
        elif settings["periodic-saving"] == 'Weekly':
            self.weekly()
        elif settings["periodic-saving"] == 'Monthly':
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
        # Check if the default folder for periodic saving exists or not
        if self.pbfolder == f'{download_dir}/SaveDesktop/archives':
            try:
                if not os.path.exists(f"{download_dir}/SaveDesktop/archives"):
                    os.makedirs(f"{download_dir}/SaveDesktop/archives")
            except:
                os.system(f"mkdir {home}/Downloads")
                os.system(f"xdg-user-dirs-update --set DOWNLOAD {home}/Downloads")
                os.makedirs(f"{download_dir}/SaveDesktop/archives")

        # Check if the path {CACHE}/periodic_saving exists or not
        if not os.path.exists(f"{CACHE}/periodic_saving"):
            os.mkdir(f"{CACHE}/periodic_saving")

        # Check if the filename format has spaces or not
        if " " in settings["filename-format"]:
            old_filename = f'{settings["filename-format"]}'
            filename = old_filename.replace(" ", "_")
        else:
            filename = settings["filename-format"]

        # Write path to the periodic saving file to the file below
        with open(f"{CACHE}/.periodicfile.json", "w") as p:
            p.write('{\n "recent_file": "%s/%s.sd.tar.gz"\n}' % (self.pbfolder, filename))
        
        # Start saving the configuration
        os.chdir(f"{CACHE}/periodic_saving")
        os.system(f"python3 {init_dir}/config.py --save")

        # Remove the file below after done saving configuration and start the self.config_saved() function
        os.system(f"rm {CACHE}/.periodicfile.json")
        self.config_saved()

    # Message about saved config
    def config_saved(self):
        os.system(f"rm -rf {CACHE}/periodic-saving/*")
        with open(f"{DATA}/periodic-saving.json", "w") as pb:
            pb.write('{\n "saving-date": "%s"\n}' % date.today())
        print("Configuration saved.")
        exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", help="Save now", action="store_true")
    args = parser.parse_args()

    pb = PeriodicBackups()
    pb.run(args.now)
