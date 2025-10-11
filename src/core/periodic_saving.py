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
            self.send_notification_at_startup()
            self.backup()
        else:
            print("MODE: Periodic saving")
            self.get_interval()

    # Send a notification about started periodic saving
    def send_notification_at_startup(self):
        try:
            self.status_desc = _("<big><b>Saving configuration …</b></big>\nThe configuration of your desktop environment will be saved in:\n <i>{}/{}.sd.tar.gz</i>\n").split('</b>')[0].split('<b>')[-1]
            subprocess.run(["notify-send", f'Save Desktop ({_("Periodic saving")})', self.status_desc])
        except NameError: # handle an error: '_' is not defined
            pass

    # Get the periodic saving interval from GSettings
    def get_interval(self):
        if settings["periodic-saving"] == 'Never':
            print("Periodic saving is not set up. Maybe you have selected Never interval in the More options dialog?")
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
            self.send_notification_at_startup()
            self.backup()
        else:
            print(f"Backup not needed today. Last backup was on {self.last_backup_date}.")

    def backup(self):
        if self.pbfolder == '{}/SaveDesktop/archives'.format(download_dir) or self.pbfolder == f'{download_dir}/SaveDesktop/archives':
            try:
                if not os.path.exists(f"{download_dir}/SaveDesktop/archives"):
                    os.makedirs(f"{download_dir}/SaveDesktop/archives")
            except FileNotFoundError:
                subprocess.run(["mkdir", f"{home}/Downloads"])
                subprocess.run([f"xdg-user-dirs-update", "--set", "DOWNLOAD", f"{home}/Downloads"])
                os.makedirs(f"{download_dir}/SaveDesktop/archives")

        if " " in settings["filename-format"]:
            self.filename = settings["filename-format"].replace(" ", "_")
        else:
            self.filename = settings["filename-format"]

        self.create_status_file()
        self.call_archive_command()
        
    # Create this file to enable some periodic saving features in archive.py
    def create_status_file(self):
        open(f"{CACHE}/pb", "w").close()

    # Call the command for making the archive
    def call_archive_command(self):
        self.archive_mode = "--create"
        self.archive_name = f"{self.pbfolder}/{self.filename}.sd.zip"

        subprocess.run([sys.executable, "-m", "savedesktop.core.archive", self.archive_mode, self.archive_name], env={**os.environ, "PYTHONPATH": f"{app_prefix}"})

        self.done()

    def done(self):
        # Save today's date to the {DATA}/periodic-saving.json file
        with open(f"{DATA}/periodic-saving.json", "w") as pb:
            json.dump({"last-saved": date.today().isoformat()}, pb)

        # Remove this file after finishing operations
        if os.path.exists(f"{CACHE}/pb"):
            os.remove(f"{CACHE}/pb")

        # Save the current periodic saving settings to the SaveDesktop.json file
        # (only for cloud drive folders)
        if os.path.exists(f"{self.pbfolder}/SaveDesktop.json"):
            open(f"{self.pbfolder}/SaveDesktop.json", "w").write('{\n "periodic-saving-interval": "%s",\n "filename": "%s"\n}' % (settings["periodic-saving"], settings["filename-format"]))

        # Send a notification about finished periodic saving
        try:
            subprocess.run(["notify-send", f'Save Desktop ({_("Periodic saving")})', _("Configuration has been saved!")])
        except NameError: # handle an error: '_' is not defined
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", help="Save now", action="store_true")
    args = parser.parse_args()

    pb = PeriodicBackups()
    pb.run(args.now)

