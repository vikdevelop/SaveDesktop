from datetime import datetime
from datetime import date
from pathlib import Path
import json
import os
import gi
from gi.repository import GLib, Gio

# get current datetime
dt = datetime.now()
# get day
current_day = datetime.today()
# get first day of month
first_day = current_day.replace(day=1)

CONFIG = f'{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/config'
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
            exit()
            
    # Periodic backups: monthly
    def monthly(self):
        if dt.day == 1:
            self.backup()
        else:
            print("Today is not first day of month.")
        
    # Create backup
    def backup(self):
        if os.path.exists('{}/SaveDesktop/archives/config_{}.sd.tar.gz'.format(download_dir, date.today())):
            print("File already exists")
            exit()
        else:
            try:
                if not os.path.exists(f"{download_dir}/SaveDesktop/archives"):
                    os.makedirs(f"{download_dir}/SaveDesktop/archives")
            except:
                os.system("mkdir ~/Downloads")
                os.system(f"xdg-user-dirs-update --set DOWNLOAD {Path.home}/Downloads")
                os.makedirs(f"{download_dir}/SaveDesktop/archives")
            os.system("mkdir -p {}/SaveDesktop/.{} && cd {}/SaveDesktop/.{}".format(download_dir, date.today(), download_dir, date.today()))
            os.chdir('{}/SaveDesktop/.{}'.format(download_dir, date.today()))
            os.system('cp ~/.config/dconf/user ./')
            os.system('cp -R ~/.local/share/backgrounds ./')
            os.system('cp -R ~/.local/share/icons ./')
            os.system('cp -R ~/.themes ./')
            os.system('cp -R ~/.icons ./')
            os.system('cp -R ~/.fonts ./')
            os.system('cp -R ~/.config/gtk-4.0 ./')
            os.system('cp -R ~/.config/gtk-3.0 ./')
            os.system('cp -R ~/.local/share/flatpak/overrides ./')
            # Save configs on individual desktop environments
            if self.environment == 'GNOME':
                os.system("cp -R ~/.local/share/gnome-background-properties ./")
                os.system("cp -R ~/.local/share/gnome-shell ./")
                os.system("cp -R ~/.local/share/nautilus-python ./")
                os.system("cp -R ~/.config/gnome-control-center ./")
            elif self.environment == 'Pantheon':
                os.system("cp -R ~/.config/plank ./")
                os.system("cp -R ~/.config/marlin ./")
            elif self.environment == 'Cinnamon':
                os.system("cp -R ~/.config/nemo ./")
                os.system("cp -R ~/.local/share/cinnamon ./")
                os.system("cp -R ~/.cinnamon ./")
            elif self.environment == 'Budgie':
                os.system("cp -R ~/.config/budgie-desktop ./")
                os.system("cp -R ~/.config/budgie-extras ./")
                os.system("cp -R ~/.config/nemo ./")
            elif self.environment == 'COSMIC':
                os.system("cp -R ~/.config/pop-shell ./")
                os.system("cp -R ~/.local/share/gnome-shell ./")
            elif self.environment == 'Xfce':
                os.system("cp -R ~/.config/xfce4 ./")
                os.system("cp -R ~/.config/Thunar ./")
                os.system("cp -R ~/.xfce4 ./")
            elif self.environment == 'MATE':
                os.system("cp -R ~/.config/caja ./")
            elif self.environment == 'KDE Plasma':
                os.system("mkdir xdg-config && mkdir xdg-data")
                os.system("cp -R ~/.config/[k]* ./xdg-config/")
                os.system("cp ~/.config/gtkrc ./xdg-config/")
                os.system("cp ~/.config/dolphinrc ./xdg-config/")
                os.system("cp ~/.config/gwenviewrc ./xdg-config/")
                os.system("cp ~/.config/plasmashellrc ./xdg-config/")
                os.system("cp ~/.config/spectaclerc ./xdg-config/")
                os.system("cp ~/.config/plasmarc ./xdg-config/")
                os.system("cp ~/.config/plasma-org.kde.plasma.desktop-appletsrc ./xdg-config/")
                os.system("cp -R ~/.local/share/[k]* ./xdg-data/")
                os.system("cp -R ~/.local/share/dolphin ./xdg-data/")
                os.system("cp -R ~/.local/share/sddm ./xdg-data/")
                os.system("cp -R ~/.local/share/wallpapers ./xdg-data/")
                os.system("cp -R ~/.local/share/plasma-systemmonitor ./xdg-data/")
            # Create Tar.gz archive
            os.system("tar --gzip -cf config_{}.sd.tar.gz ./".format(date.today()))
            self.move_tarball()
            self.config_saved()
    
    # Move tarball to ~/Downloads/SaveDesktop/archives/
    def move_tarball(self):
        os.chdir('{}/SaveDesktop/.{}'.format(download_dir, date.today()))
        os.system("mv ./*.tar.gz {}/SaveDesktop/archives/".format(download_dir))
      
    # Message about saved config
    def config_saved(self):
        os.system("rm -rf {}/SaveDesktop/.{}/*".format(download_dir, date.today()))
        print("Configuration saved.")
    
PeriodicBackups()
