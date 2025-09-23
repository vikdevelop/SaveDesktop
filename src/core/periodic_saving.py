import argparse, json, os, gi, shutil, subprocess, sys
from datetime import datetime, date, timedelta
from pathlib import Path
from gi.repository import GLib, Gio
from savedesktop.globals import *
from savedesktop.core.password_store import PasswordStore

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
            print("Saving immediately")
            self.backup()
        else:
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
        if self.pbfolder == f'{download_dir}/SaveDesktop/archives':
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

        os.makedirs(f"{CACHE}/periodic_saving", exist_ok=True)
        os.chdir(f"{CACHE}/periodic_saving")
        os.system("echo > saving_status")
        subprocess.run([sys.executable, "-m", "savedesktop.core.config", "--save"], check=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})

        print("creating the configuration archive")
        print("moving the configuration archive to the user-defined directory")
        self.get_password_from_file()

        self.save_last_backup_date()
        self.config_saved()
        
    # Get an encrypted password from the {DATA}/password file
    def get_password_from_file(self):
        try:
            ps = PasswordStore()
            self.password = ps.password
        except:
            self.password = None
        if self.password != None:
           subprocess.run(['7z', 'a', '-tzip', '-mx=6', f'-p{self.password}', '-mem=AES256', '-x!*.zip', '-x!saving_status', 'cfg.sd.zip', '.'], check=True)
        else:
           subprocess.run(['7z', 'a', '-tzip', '-mx=6', '-x!*.zip', '-x!saving_status', 'cfg.sd.zip', '.'], check=True)
        shutil.copyfile('cfg.sd.zip', f'{self.pbfolder}/{self.filename}.sd.zip')

    # Save today's date to the {DATA}/periodic-saving.json file
    def save_last_backup_date(self):
        with open(f"{DATA}/periodic-saving.json", "w") as pb:
            json.dump({"last-saved": date.today().isoformat()}, pb)

    def config_saved(self):
        os.chdir(CACHE)
        shutil.rmtree("periodic_saving")
        print("Configuration saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", help="Save now", action="store_true")
    args = parser.parse_args()

    pb = PeriodicBackups()
    pb.run(args.now)

