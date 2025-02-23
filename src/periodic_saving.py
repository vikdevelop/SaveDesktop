import argparse, json, os, gi, shutil, subprocess
from datetime import datetime, date, timedelta
from pathlib import Path
from gi.repository import GLib, Gio
from localization import _, CACHE, DATA, home, system_dir, settings, download_dir, snap

# Get the current date
dt = datetime.now()

# Get the current day
current_day = datetime.today()

# Get the first day of month
first_day = current_day.replace(day=1)

class PeriodicBackups:
    def __init__(self):
        self.last_backup_date = self.load_last_backup_date()

    def load_last_backup_date(self):
        backup_file = f"{DATA}/periodic-saving.json"
        if os.path.exists(backup_file):
            with open(backup_file) as pb:
                jp = json.load(pb)
            return date.fromisoformat(jp.get("last-saved", "2000-01-01"))
        return date(2000, 1, 1)

    def run(self, now: bool) -> None:
        if settings["periodic-saving-folder"] == '':
            self.pbfolder = f'{download_dir}/SaveDesktop/archives'
        else:
            self.pbfolder = f'{settings["periodic-saving-folder"]}'

        if now:
            print("Saving immediately")
            self.backup()
        else:
            self.get_interval()

    def get_interval(self):
        if settings["periodic-saving"] == 'Never':
            print("Periodic saving is not set up.")
            exit()
        elif settings["periodic-saving"] == 'Daily':
            self.check_and_backup(1)
        elif settings["periodic-saving"] == 'Weekly':
            self.check_and_backup(7)
        elif settings["periodic-saving"] == 'Monthly':
            self.check_and_backup(30)

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
            filename = settings["filename-format"].replace(" ", "_")
        else:
            filename = settings["filename-format"]

        os.makedirs(f"{CACHE}/periodic_saving", exist_ok=True)
        os.chdir(f"{CACHE}/periodic_saving")
        os.system("echo > saving_status")
        os.system(f"python3 {system_dir}/config.py --save")

        print("creating the configuration archive")
        os.system(f"tar --exclude='cfg.sd.tar.gz' --exclude='saving_status' --gzip -cf cfg.sd.tar.gz ./")
        print("moving the configuration archive to the user-defined directory")
        shutil.copyfile('cfg.sd.tar.gz', f'{self.pbfolder}/{filename}.sd.tar.gz')

        self.save_last_backup_date()
        self.config_saved()

    def save_last_backup_date(self):
        with open(f"{DATA}/periodic-saving.json", "w") as pb:
            json.dump({"last-saved": date.today().isoformat()}, pb)

    def config_saved(self):
        os.system(f"rm -rf {CACHE}/periodic-saving/*")
        os.system("rm saving_status")
        print("Configuration saved.")
        exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", help="Save now", action="store_true")
    args = parser.parse_args()

    pb = PeriodicBackups()
    pb.run(args.now)
