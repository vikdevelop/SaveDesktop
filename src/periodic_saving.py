from datetime import datetime
from datetime import date
from pathlib import Path
import json
import os
import gi
from gi.repository import GLib, Gio
from localization import _, CACHE, home

# get current datetime
dt = datetime.now()
# get day
current_day = datetime.today()
# get first day of month
first_day = current_day.replace(day=1)

download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)

class PeriodicBackups:
    def __init__(self):
        # check of user current desktop
        if os.getenv('XDG_CURRENT_DESKTOP') == 'GNOME':
            self.environment = 'GNOME'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'zorin:GNOME':
            self.environment = 'GNOME'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'ubuntu:GNOME':
            self.environment = 'GNOME'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
            self.environment = 'COSMIC'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Pantheon':
            self.environment = 'Pantheon'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'X-Cinnamon':
            self.environment = 'Cinnamon'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Budgie:GNOME':
            self.environment = 'Budgie'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
            self.environment = 'Xfce'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'MATE':
            self.environment = 'MATE'
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
            self.environment = 'KDE Plasma'
        
        self.settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
        
        # Get directory for storing periodic backups
        if self.settings["periodic-saving-folder"] == '':
            self.pbfolder = f'{download_dir}/SaveDesktop/archives'
        else:
            self.pbfolder = f'{self.settings["periodic-saving-folder"]}'
        
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
        if not os.path.exists(f"{CACHE}/periodic-saving"):
        	os.mkdir(f"{CACHE}/periodic-saving")
        os.chdir(f"{CACHE}/periodic-saving")
        os.system("dconf dump / > ./dconf-settings.ini")
        #os.system('cp -R {home}/.config/dconf/user ./')
        os.system(f'cp -R {home}/.config/gtk-4.0 ./')
        os.system(f'cp -R {home}/.config/gtk-3.0 ./')
        if self.settings["save-backgrounds"] == True:
            os.system(f'cp -R {home}/.local/share/backgrounds ./')
        if self.settings["save-icons"] == True:
            os.system(f'cp -R {home}/.local/share/icons ./')
            os.system(f'cp -R {home}/.icons ./')
        if self.settings["save-themes"] == True:
            os.system(f'cp -R {home}/.themes ./')
        if self.settings["save-fonts"] == True:
            os.system(f'cp -R {home}/.fonts ./')
        if self.settings["save-installed-flatpaks"] == True:
            os.system('sh /app/backup_flatpaks.sh')
        # Save configs on individual desktop environments
        if self.environment == 'GNOME':
            os.system(f"cp -R {home}/.local/share/gnome-background-properties ./")
            os.system(f"cp -R {home}/.local/share/gnome-shell ./")
            os.system(f"cp -R {home}/.local/share/nautilus-python ./")
            os.system(f"cp -R {home}/.config/gnome-control-center ./")
        elif self.environment == 'Pantheon':
            os.system(f"cp -R {home}/.config/plank ./")
            os.system(f"cp -R {home}/.config/marlin ./")
        elif self.environment == 'Cinnamon':
            os.system(f"cp -R {home}/.config/nemo ./")
            os.system(f"cp -R {home}/.local/share/cinnamon ./")
            os.system(f"cp -R {home}/.cinnamon ./")
        elif self.environment == 'Budgie':
            os.system(f"cp -R {home}/.config/budgie-desktop ./")
            os.system(f"cp -R {home}/.config/budgie-extras ./")
            os.system(f"cp -R {home}/.config/nemo ./")
        elif self.environment == 'COSMIC':
            os.system(f"cp -R {home}/.config/pop-shell ./")
            os.system(f"cp -R {home}/.local/share/gnome-shell ./")
        elif self.environment == 'Xfce':
            os.system(f"cp -R {home}/.config/xfce4 ./")
            os.system(f"cp -R {home}/.config/Thunar ./")
            os.system(f"cp -R {home}/.xfce4 ./")
        elif self.environment == 'MATE':
            os.system(f"cp -R {home}/.config/caja ./")
        elif self.environment == 'KDE Plasma':
            os.system("mkdir xdg-config && mkdir xdg-data")
            os.system(f"cp -R {home}/.config/[k]* ./xdg-config/")
            os.system(f"cp {home}/.config/gtkrc ./xdg-config/")
            os.system(f"cp {home}/.config/dolphinrc ./xdg-config/")
            os.system(f"cp {home}/.config/gwenviewrc ./xdg-config/")
            os.system(f"cp {home}/.config/plasmashellrc ./xdg-config/")
            os.system(f"cp {home}/.config/spectaclerc ./xdg-config/")
            os.system(f"cp {home}/.config/plasmarc ./xdg-config/")
            os.system(f"cp {home}/.config/plasma-org.kde.plasma.desktop-appletsrc ./xdg-config/")
            os.system(f"cp -R {home}/.local/share/[k]* ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/dolphin ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/sddm ./xdg-data/")
            if self.settings["save-backgrounds"] == True:
                os.system(f"cp -R {home}/.local/share/wallpapers ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/plasma-systemmonitor ./xdg-data/")
        if " " in self.settings["filename-format"]:
            old_filename = f'{self.settings["filename-format"]}'
            filename = old_filename.replace(" ", "_")
        else:
            filename = self.settings["filename-format"]
        # Create Tar.gz archive
        os.system(f"tar --gzip -cf {filename}.sd.tar.gz ./")
        os.system("mv ./*.tar.gz {}/".format(self.pbfolder))
        self.config_saved()
      
    # Message about saved config
    def config_saved(self):
        os.system(f"rm -rf {CACHE}/periodic-saving/*")
        print("Configuration saved.")
        exit()
    
PeriodicBackups()
