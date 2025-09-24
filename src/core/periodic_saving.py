import argparse, json, os, gi, shutil, subprocess, sys
from datetime import datetime, date, timedelta
from pathlib import Path
from gi.repository import GLib, Gio
from savedesktop.globals import *

# Get the current date
dt = datetime.now()

# Get the current day
current_day = datetime.today()

# Get the first day of month
first_day = current_day.replace(day=1)

class PeriodicBackups:
    def __init__(self):
        self.last_backup_date = self.load_last_backup_date()

    # Load last backup date from the {DATA}/periodic-saving.json file
    def load_last_backup_date(self):
        backup_file = f"{DATA}/periodic-saving.json"
        if os.path.exists(backup_file):
            with open(backup_file) as pb:
                jp = json.load(pb)
            return date.fromisoformat(jp.get("last-saved", "2000-01-01"))
        return date(2000, 1, 1)

    # Start periodic saving without checking last backup date (with --now parameter)
    # or with checking it
    def run(self, now: bool) -> None:
        self.pbfolder = f'{settings["periodic-saving-folder"].format(download_dir)}'

        if now:
            print("MODE: Save now")
            self.backup()
        else:
            print("MODE: Periodic saving")
            self.get_interval()

    # Get the periodic saving interval from GSettings
    def get_interval(self):
        if settings["periodic-saving"] == 'Never':
            print("Periodic saving is not set up.")
        elif settings["periodic-saving"] == 'Daily':
            self.check_and_backup(1)
        elif settings["periodic-saving"] == 'Weekly':
            self.check_and_backup(7)
        elif settings["periodic-saving"] == 'Monthly':
            self.check_and_backup(30)

    # Check the number of days since the last backup
    def check_and_backup(self, interval):
        today = date.today()
        if (today - self.last_backup_date).days >= interval:
            self.backup()
        else:
            print(f"Backup not needed today. Last backup was on {self.last_backup_date}.")

    def backup(self):
        if self.pbfolder == '{}/SaveDesktop/archives'.format(download_dir) or self.pbfolder == f'{download_dir}/SaveDesktop/archives':
            try:
                if not os.path.exists(f"{download_dir}/SaveDesktop/archives"):
                    os.makedirs(f"{download_dir}/SaveDesktop/archives")
            except:
                os.system(f"mkdir {home}/Downloads")
                os.system(f"xdg-user-dirs-update --set DOWNLOAD {home}/Downloads")
                os.makedirs(f"{download_dir}/SaveDesktop/archives")

        if " " in settings["filename-format"]:
            self.filename = settings["filename-format"].replace(" ", "_")
        else:
            self.filename = settings["filename-format"]

        self.call_archive_command()

        self.save_last_backup_date()
        self.config_saved()
        
    # Call the command for making the archive
    def call_archive_command(self):
        self.archive_mode = "--create"
        self.archive_name = f"{self.pbfolder}/{self.filename}"

        subprocess.run([sys.executable, "-m", "savedesktop.core.archive", self.archive_mode, self.archive_name], env={**os.environ, "PYTHONPATH": f"{app_prefix}"})

    # Save today's date to the {DATA}/periodic-saving.json file
    def save_last_backup_date(self):
        with open(f"{DATA}/periodic-saving.json", "w") as pb:
            json.dump({"last-saved": date.today().isoformat()}, pb)

    def config_saved(self):
        print("Configuration saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", help="Save now", action="store_true")
    args = parser.parse_args()

    pb = PeriodicBackups()
    pb.run(args.now)

