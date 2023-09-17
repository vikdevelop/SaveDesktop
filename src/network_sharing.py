#!/usr/bin/python3
from pathlib import Path
from datetime import datetime
from datetime import date
import os
import locale
import json
import gi
import socket
import shutil
from gi.repository import Gio, GLib

# Load system language
p_lang = locale.getlocale()[0]
if p_lang == 'pt_BR':
    r_lang = 'pt_BR'
elif p_lang == 'nb_NO':
    r_lang = 'nb_NO'
elif 'zh' in p_lang:
    r_lang = 'zh_Hans'
else:
    r_lang = p_lang[:-3]
    
try:
    locale = open(f"/app/translations/{r_lang}.json")
except:
    locale = open("/app/translations/en.json")
    
_ = json.load(locale)

# Get IP adress of user computer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IPAddr = s.getsockname()[0]
s.close()

dt = datetime.now()

settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
CACHE = f'{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp'
DATA = f'{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data'
system_dir = "/app"

os.system(f"rm -rf {CACHE}/*")

# Check if syncing directory exists
if not os.path.exists(f"{CACHE}/syncing"):
    os.mkdir(f"{CACHE}/syncing")
    
# Check of user current desktop environment
if os.getenv('XDG_CURRENT_DESKTOP') == 'GNOME':
    environment = 'GNOME'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'zorin:GNOME':
    environment = 'GNOME'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'ubuntu:GNOME':
    environment = 'GNOME'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
    environment = 'COSMIC'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'Pantheon':
    environment = 'Pantheon'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'X-Cinnamon':
    environment = 'Cinnamon'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'Budgie:GNOME':
    environment = 'Budgie'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
    environment = 'Xfce'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'MATE':
    environment = 'MATE'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
    environment = 'KDE Plasma'

class Syncing:
    def __init__(self):
        # Check if user has same or empty IP adress property
        if IPAddr in settings["url-for-syncing"]:
            print("You have same IP adress.")
        elif settings["url-for-syncing"] == "":
            self.get_sync_type()
            print("Synchronization is not set up.")
        else:
            self.get_file_info()

    # Get info about synchronization
    def get_file_info(self):
        # Download file-settings.json file to getting information about it
        os.chdir(f"{CACHE}/syncing")
        os.system(f"wget {settings['url-for-syncing']}/file-settings.json")
        with open("file-settings.json") as j:
            self.jF = json.load(j)
        self.file = self.jF["file-name"]
        if self.jF["periodic-import"] == "Never2":
            self.get_sync_type()
            print("Synchronization is not set up.")
        elif self.jF["periodic-import"] == "Daily2":
            self.get_sync_type()
            self.check_sync()()
        elif self.jF["periodic-import"] == "Weekly2":
            self.get_sync_type()
            if date.today().weekday() == 1:
                self.self.check_sync()
            else:
                print("Today is not Tuesday.")
        elif self.jF["periodic-import"] == "Monthly2":
            self.get_sync_type()
            if dt.day == 2:
                self.self.check_sync()
            else:
                print("Today is not second day of month.")
        elif self.jF["periodic-import"] == "Manually2":
            self.get_sync_type_not()
            self.check_sync()
            
    def get_sync_type(self):
        if settings["manually-sync"] == True:
            settings["manually-sync"] = False

    def get_sync_type_not(self):
        if settings["manually-sync"] == False:
            settings["manually-sync"] = True

    def check_sync(self):
        if os.path.exists(f"{DATA}/sync-info.json"):
            with open(f"{DATA}/sync-info.json") as s:
                jl = json.load(s)
            if jl["sync-date"] == f'{date.today()}':
                print("The configuration has already been imported today.")
                exit()
            else:
                self.download_config()
        else:
            self.download_config()
               
    # Download archive from URL
    def download_config(self):
        os.system(f"wget {settings['url-for-syncing']}/{self.file}")
        if os.path.exists(f"{self.file}"):
            os.system(f"tar -xf {self.file} ./")
        else:
            os.system(f"tar -xf {self.file}.1 ./")
        
        # Create Dconf directory
        if not os.path.exists("{}/.config/dconf".format(Path.home())):
            os.mkdir(f"{Path.home()}/.config/dconf")
        else:
            shutil.rmtree(f"{Path.home()}/.config/dconf")
            os.mkdir(f"{Path.home()}/.config/dconf")
        
        self.import_config()
            
    # Import configuration
    def import_config(self):
        # Applying configuration for GNOME-based environments
        if not os.path.exists("{}/.config".format(Path.home())):
            os.system("mkdir ~/.config/")
        os.system(f"cp ./user {Path.home()}/.config/dconf/")
        os.system(f'cp -R ./icons {Path.home()}/.local/share/')
        os.system(f'cp -R ./.themes {Path.home()}/')
        os.system(f'cp -R ./.icons {Path.home()}/')
        os.system(f'cp -R ./backgrounds {Path.home()}/.local/share/')
        os.system(f'cp -R ./.fonts {Path.home()}/')
        os.system(f'cp -R ./gtk-4.0 {Path.home()}/.config/')
        os.system(f'cp -R ./gtk-3.0 {Path.home()}/.config/')
        os.system(f'cp ./installed_flatpaks.sh {DATA}/')
        # Apply configs for individual desktop environments
        if environment == 'GNOME':
            os.system(f'cp -R ./gnome-background-properties {Path.home()}/.local/share/')
            os.system(f'cp -R ./gnome-shell {Path.home()}/.local/share/')
            os.system(f'cp -R ./nautilus-python {Path.home()}/.local/share/')
            os.system(f'cp -R ./gnome-control-center {Path.home()}/.config/')
        elif environment == 'Pantheon':
            os.system(f'cp -R ./plank {Path.home()}/.config/')
            os.system(f'cp -R ./marlin {Path.home()}/.config/')
        elif environment == 'Cinnamon':
            os.system(f'cp -R ./nemo {Path.home()}/.config/')
            os.system(f'cp -R ./cinnamon {Path.home()}/.local/share/')
            os.system(f'cp -R ./.cinnamon {Path.home()}/')
        elif environment == 'Budgie':
            os.system(f'cp -R ./budgie-desktop {Path.home()}/.config/')
            os.system(f'cp -R ./budgie-extras {Path.home()}/.config/')
            os.system(f'cp -R ./nemo {Path.home()}/.config/')
        elif environment == 'COSMIC':
            os.system(f'cp -R ./pop-shell {Path.home()}/.config/')
            os.system(f'cp -R ./gnome-shell {Path.home()}/.local/share/')
        elif environment == 'Xfce':
            os.system(f'cp -R ./xfce4 {Path.home()}/.config/')
            os.system(f'cp -R ./Thunar {Path.home()}/.config/')
            os.system(f'cp -R ./.xfce4 {Path.home()}/')
        elif environment == 'MATE':
            os.system(f'cp -R ./caja {Path.home()}/.config/')
        elif environment == 'KDE Plasma':
            os.chdir("%s/syncing" % CACHE)
            os.chdir('xdg-config')
            os.system(f'cp -R ./ {Path.home()}/.config/')
            os.chdir("%s/syncing" % CACHE)
            os.chdir('xdg-data')
            os.system(f'cp -R ./ {Path.home()}/.local/share/')
        self.create_flatpak_desktop()
        self.done()
        
    def create_flatpak_desktop(self):
        os.system(f"cp {system_dir}/install_flatpak_from_script.py {DATA}/")
        if not os.path.exists(f"{Path.home()}/.config/autostart"):
            os.mkdir(f"{Path.home()}/.config/autostart")
        if not os.path.exists(f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"):
            with open(f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as fa:
                fa.write(f"[Desktop Entry]\nName=SaveDesktop (Flatpak Apps installer)\nType=Application\nExec=python3 {DATA}/install_flatpak_from_script.py")
                
    def done(self):
        with open(f"{DATA}/sync-info.json", "w") as s:
            s.write('{\n "sync-date": "%s"\n}' % date.today())
        os.system(f"rm -rf {CACHE}/syncing/*")
        print("Configuration has been synced successfully.")
        os.system(f"notify-send 'SaveDesktop ({self.file[:-10]})' '{_['config_imported']} {_['periodic_saving_desc']}' -i io.github.vikdevelop.SaveDesktop-symbolic")
        #os.system("pkill -15 python3 && pkill -15 python")

Syncing()

