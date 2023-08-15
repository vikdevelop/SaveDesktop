#!/usr/bin/python3
from pathlib import Path
from datetime import datetime
from datetime import date
import os
import locale
import json
import gi
import socket
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
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

dt = datetime.now()

settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
CACHE = f'{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp'
DATA = f'{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data'
system_dir = "/app"

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
            print("Synchronization is not set up.")
        else:
            self.path = Path(settings["file-for-syncing"])
            self.folder = self.path.parent.absolute()
            
            # Download file-settings.json file to getting information about it
            os.chdir(f"{CACHE}/syncing")
            os.system(f"wget {settings['url-for-syncing']}/file-settings.json")
            with open("file-settings.json") as j:
                self.jF = json.load(j)
            self.file = self.jF["file-name"]
            if self.jF["periodic-import"] == _["never"]:
                print("Synchronization is not set up.")
            elif self.jF["periodic-import"] == _["daily"]:
                self.download_config()
            elif self.jF["periodic-import"] == _["weekly"]:
                if date.today().weekday() == 1:
                    self.download_config()
                else:
                    print("Today is not Tuesday.")
            elif jF["periodic-import"] == _["monthly"]:
                if dt.day == 10:
                    self.download_config()
                else:
                    print("Today is not tenth day of month.")
               
    # Download file from URL
    def download_config(self):
        os.system(f"wget {settings['url-for-syncing']}/{self.file}")
        if os.path.exists(f"{self.file}"):
            os.system(f"tar -xf {self.file} ./")
        else:
            os.system(f"tar -xf {self.file}.1 ./")
                
        if os.path.exists(".file-settings.json"):
            print("The configuration has already been imported today.")
            exit()
        else:
            self.import_config()
            
    # Import configuration
    def import_config(self):
        # Applying configuration for GNOME-based environments
        if not os.path.exists("{}/.config".format(Path.home())):
            os.system("mkdir ~/.config/")
        # Create Dconf directory
        os.system("rm -rf ~/.config/dconf && mkdir ~/.config/dconf")
        self.i_dconf = GLib.spawn_command_line_async(f"cp ./user {Path.home()}/.config/dconf/")
        self.i_icons = GLib.spawn_command_line_async(f'cp -R ./icons {Path.home()}/.local/share/')
        self.i_themes = GLib.spawn_command_line_async(f'cp -R ./.themes {Path.home()}/')
        self.i_icons_home = GLib.spawn_command_line_async(f'cp -R ./.icons {Path.home()}/')
        self.i_backgrounds = GLib.spawn_command_line_async(f'cp -R ./backgrounds {Path.home()}/.local/share/')
        self.i_fonts = GLib.spawn_command_line_async(f'cp -R ./.fonts {Path.home()}/')
        self.i_gtk4 = GLib.spawn_command_line_async(f'cp -R ./gtk-4.0 {Path.home()}/.config/')
        self.i_gtk3 = GLib.spawn_command_line_async(f'cp -R ./gtk-3.0 {Path.home()}/.config/')
        self.flatpak_apps = GLib.spawn_command_line_async(f'cp ./installed_flatpaks.sh {DATA}/')
        # Apply configs for individual desktop environments
        if environment == 'GNOME':
            self.i_background_properties = GLib.spawn_command_line_async(f'cp -R ./gnome-background-properties {Path.home()}/.local/share/')
            self.i_gshell = GLib.spawn_command_line_async(f'cp -R ./gnome-shell {Path.home()}/.local/share/')
            self.i_nautilus = GLib.spawn_command_line_async(f'cp -R ./nautilus-python {Path.home()}/.local/share/')
            self.i_gccenter = GLib.spawn_command_line_async(f'cp -R ./gnome-control-center {Path.home()}/.config/')
        elif environment == 'Pantheon':
            self.i_plank = GLib.spawn_command_line_async(f'cp -R ./plank {Path.home()}/.config/')
            self.i_marlin = GLib.spawn_command_line_async(f'cp -R ./marlin {Path.home()}/.config/')
        elif environment == 'Cinnamon':
            self.i_nemo = GLib.spawn_command_line_async(f'cp -R ./nemo {Path.home()}/.config/')
            self.i_cinnamon_data = GLib.spawn_command_line_async(f'cp -R ./cinnamon {Path.home()}/.local/share/')
            self.i_cinnamon_home = GLib.spawn_command_line_async(f'cp -R ./.cinnamon {Path.home()}/')
        elif environment == 'Budgie':
            self.i_budgie_desktop = GLib.spawn_command_line_async(f'cp -R ./budgie-desktop {Path.home()}/.config/')
            self.i_budgie_extras = GLib.spawn_command_line_async(f'cp -R ./budgie-extras {Path.home()}/.config/')
            self.i_nemo_b = GLib.spawn_command_line_async(f'cp -R ./nemo {Path.home()}/.config/')
        elif environment == 'COSMIC':
            self.i_popshell = GLib.spawn_command_line_async(f'cp -R ./pop-shell {Path.home()}/.config/')
            self.i_gshell_pop = GLib.spawn_command_line_async(f'cp -R ./gnome-shell {Path.home()}/.local/share/')
        elif environment == 'Xfce':
            self.i_xfconf = GLib.spawn_command_line_async(f'cp -R ./xfce4 {Path.home()}/.config/')
            self.i_thunar = GLib.spawn_command_line_async(f'cp -R ./Thunar {Path.home()}/.config/')
            self.i_xfhome = GLib.spawn_command_line_async(f'cp -R ./.xfce4 {Path.home()}/')
        elif environment == 'MATE':
            self.i_caja = GLib.spawn_command_line_async(f'cp -R ./caja {Path.home()}/.config/')
        elif environment == 'KDE Plasma':
            os.chdir("%s/syncing" % CACHE)
            os.chdir('xdg-config')
            self.i_kconf = GLib.spawn_command_line_async(f'cp -R ./ {Path.home()}/.config/')
            os.chdir("%s/syncing" % CACHE)
            os.chdir('xdg-data')
            self.i_kdata = GLib.spawn_command_line_async(f'cp -R ./ {Path.home()}/.local/share/')
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
        os.system("mv file-settings.json .file-settings.json")
        os.system(f"rm -rf {CACHE}/syncing/*")
        print("Configuration has been synced successfully.")
        os.system(f"notify-send 'SaveDesktop' '{_['config_imported']} ({self.file[:-7]})' -i io.github.vikdevelop.SaveDesktop")
        #os.system("pkill -15 python3 && pkill -15 python")

Syncing()
