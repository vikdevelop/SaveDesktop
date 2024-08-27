import os
import json
import gi
import subprocess
import zipfile
import tarfile
from gi.repository import GLib, Gio
from localization import _, CACHE, DATA, home, system_dir, flatpak, snap
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save", help="Save the current configuration", action="store_true")
parser.add_argument("-i", "--import_", help="Import saved configuration", action="store_true")

args = parser.parse_args()

# check of user current desktop
if os.getenv('XDG_CURRENT_DESKTOP') == 'GNOME':
    environment = 'GNOME'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'zorin:GNOME':
    environment = 'GNOME'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'ubuntu:GNOME':
    environment = 'GNOME'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
    environment = 'COSMIC (Old)'
elif os.getenv('XDG_CURRENT_DESKTOP') == 'COSMIC':
    environment = 'COSMIC (New)'
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
elif os.getenv('XDG_CURRENT_DESKTOP') == 'Deepin':
    environment = 'Deepin'
else:
    from tty_environments import *
    
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
cache_replacing = f'{CACHE}'
config = cache_replacing.replace("cache/tmp", "config/glib-2.0/settings")
flatpak_app_data = settings["disabled-flatpak-apps-data"]

class Save:
    def __init__(self):
        # create a txt file to prevent deleting the current saving by closing the application window
        os.system("echo > saving_status")
        print("saving settings from the Dconf database")
        os.system("dconf dump / > ./dconf-settings.ini")
        print("saving Gtk settings")
        os.system(f'cp -R {home}/.config/gtk-4.0 ./')
        os.system(f'cp -R {home}/.config/gtk-3.0 ./')
        if settings["save-backgrounds"] == True:
            print("saving backgrounds")
            os.system(f'cp -R {home}/.local/share/backgrounds ./')
        if settings["save-icons"] == True:
            print("saving icons")
            os.system(f'cp -R {home}/.local/share/icons ./')
            os.system(f'cp -R {home}/.icons ./')
        if settings["save-themes"] == True:
            print("saving themes")
            os.system(f'cp -R {home}/.themes ./')
            os.system(f'cp -R {home}/.local/share/themes ./')
        if settings["save-fonts"] == True:
            print("saving fonts")
            os.system(f'cp -R {home}/.fonts ./')
            os.system(f'cp -R {home}/.local/share/fonts ./')
        if settings["save-desktop-folder"] == True:
            print("saving desktop folder")
            if " " in GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP):
                desktop_with_spaces = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)
                desktop_without_spaces = desktop_with_spaces.replace(" ", "*")
            else:
                desktop_without_spaces = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)
            os.system(f'cp -R {desktop_without_spaces} ./Desktop/ ')
        if flatpak:
            if settings["save-installed-flatpaks"] == True:
                print("saving list of installed Flatpak apps")
                os.system("ls /var/lib/flatpak/app/ | awk '{print \"flatpak install --system \" $1 \" -y\"}' > ./installed_flatpaks.sh")
                os.system("ls ~/.local/share/flatpak/app | awk '{print \"flatpak install --user \" $1 \" -y\"}' > ./installed_user_flatpaks.sh")
        if settings["save-flatpak-data"] == True:
            print("saving user data of installed Flatpak apps")
            self.save_flatpak_data()
            
        print("saving desktop environment configuration files")
        # Save configs on individual desktop environments
        if environment == 'GNOME':
            os.system(f"cp -R {home}/.local/share/gnome-background-properties ./")
            if settings["save-extensions"] == True:
                os.system(f"cp -R {home}/.local/share/gnome-shell ./")
            os.system(f"cp -R {home}/.local/share/nautilus-python ./")
            os.system(f"cp -R {home}/.local/share/nautilus ./")
            os.system(f"cp -R {home}/.config/gnome-control-center ./")
        elif environment == 'Pantheon':
            os.system(f"cp -R {home}/.config/plank ./")
            os.system(f"cp -R {home}/.config/marlin ./")
        elif environment == 'Cinnamon':
            os.system(f"cp -R {home}/.config/nemo ./")
            if settings["save-extensions"] == True:
                os.system(f"cp -R {home}/.local/share/cinnamon ./")
            os.system(f"cp -R {home}/.cinnamon ./")
        elif environment == 'Budgie':
            os.system(f"cp -R {home}/.config/budgie-desktop ./")
            os.system(f"cp -R {home}/.config/budgie-extras ./")
            os.system(f"cp -R {home}/.config/nemo ./")
        elif environment == 'COSMIC (Old)':
            os.system(f"cp -R {home}/.config/pop-shell ./")
            os.system(f"cp -R {home}/.local/share/gnome-shell ./")
            os.system(f"cp -R {home}/.local/share/nautilus")
        elif environment == 'COSMIC (New)':
            os.system(f"cp -R {home}/.config/cosmic ./")
            os.system(f"cp -R {home}/.local/state/cosmic ./cosmic-state")
        elif environment == 'Xfce':
            os.system(f"cp -R {home}/.config/xfce4 ./")
            os.system(f"cp -R {home}/.config/Thunar ./")
            os.system(f"cp -R {home}/.xfce4 ./")
        elif environment == 'MATE':
            os.system(f"cp -R {home}/.config/caja ./")
        elif environment == 'KDE Plasma':
            os.system("mkdir xdg-config && mkdir xdg-data")
            os.system(f"cp -R {home}/.config/[k]* ./xdg-config/")
            os.system(f"cp {home}/.config/gtkrc ./xdg-config/")
            os.system(f"cp {home}/.config/dolphinrc ./xdg-config/")
            os.system(f"cp {home}/.config/gwenviewrc ./xdg-config/")
            os.system(f"cp {home}/.config/plasmashellrc ./xdg-config/")
            os.system(f"cp {home}/.config/spectaclerc ./xdg-config/")
            os.system(f"cp {home}/.config/plasmarc ./xdg-config/")
            os.system(f"cp {home}/.config/plasma-org.kde.plasma.desktop-appletsrc ./xdg-config/")
            os.system(f"cp -R {home}/.config/Kvantum ./xdg-config/")
            os.system(f"cp -R {home}/.config/latte ./xdg-config/")
            os.system(f"cp -R {home}/.local/share/[k]* ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/dolphin ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/sddm ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/aurorae ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/plasma-systemmonitor ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/color-schemes ./xdg-data/")
            if settings["save-backgrounds"] == True:
                os.system(f"cp -R {home}/.local/share/wallpapers ./xdg-data/")
            if settings["save-extensions"] == True:
                os.system(f"cp -R {home}/.local/share/plasma ./xdg-data/")
        elif environment == 'Deepin':
            os.system(f"cp -R {home}/.config/deepin ./")
            os.system(f"cp -R {home}/.local/share/deepin ./deepin-data")
        print("creating configuration archive")
        if os.path.exists(f"{CACHE}/.filedialog.json"):
            with open(f"{CACHE}/.filedialog.json") as j:
                j = json.load(j)
            if settings["enable-encryption"] == True:
                password = subprocess.getoutput(f"cat {CACHE}/.pswd_temp")
                os.system(f"zip -9 -P '{password}' cfg.sd.zip . -r -x 'saving_status'")
                print("moving the configuration archive to the user-defined directory")
            else:
                os.system(f"tar --exclude='cfg.sd.tar.gz' --exclude='saving_status' --gzip -cf cfg.sd.tar.gz ./")
                print("moving the configuration archive to the user-defined directory")
        elif os.path.exists(f"{CACHE}/.periodicfile.json"):
            os.system(f"tar --exclude='cfg.sd.tar.gz' --exclude='saving_status' --gzip -cf cfg.sd.tar.gz ./")
            print("moving the configuration archive to the user-defined directory")
            with open(f"{CACHE}/.periodicfile.json") as j:
                j = json.load(j)
            shutil.copyfile('cfg.sd.tar.gz', j['recent_file'])
            if not settings["periodic-import"] == "Never2":
                if "fuse" in subprocess.getoutput(f"df -T \"{settings['periodic-saving-folder']}\""):
                    os.path.exists(f"{settings['periodic-saving-folder']}/SaveDesktop-sync-file") and os.remove(f"{settings['periodic-saving-folder']}/SaveDesktop-sync-file")
                    with open(f"{settings['periodic-saving-folder']}/SaveDesktop.json", "w") as pf:
                        pf.write('{\n "periodic-saving-interval": "%s",\n "periodic-saving-folder": "%s",\n "filename": "%s"\n}' % (settings["periodic-saving"], settings["periodic-saving-folder"], settings["filename-format"]))
        print("THE CONFIGURATION HAS BEEN SAVED SUCCESSFULLY!")
        os.system("rm saving_status")
    
    # save Flatpak apps data
    def save_flatpak_data(self):
        blst = settings["disabled-flatpak-apps-data"]
        # convert GSettings property to a list
        blacklist = blst
        
        # set destination dir
        if os.path.exists(f"{CACHE}/.periodicfile.json"):
            os.makedirs(f"{CACHE}/periodic_saving/app", exist_ok=True)
            destdir = f"{CACHE}/periodic_saving/app"
        elif os.path.exists(f"{CACHE}/.filedialog.json"):
            os.makedirs(f"{CACHE}/save_config/app", exist_ok=True)
            destdir = f"{CACHE}/save_config/app"
        
        # copy Flatpak apps data
        for item in os.listdir(f"{home}/.var/app"):
            if item not in blacklist and item != "cache":  # Exclude 'cache' directory
                source_path = os.path.join(f"{home}/.var/app", item)
                destination_path = os.path.join(destdir, item)
                if os.path.isdir(source_path):
                    try:
                        shutil.copytree(source_path, destination_path, ignore=shutil.ignore_patterns('cache'))  # Ignore 'cache' in subdirectories
                    except Exception as e:
                        print(f"Error copying directory {source_path}: {e}")
                else:
                    try:
                        shutil.copy2(source_path, destination_path)
                    except Exception as e:
                        print(f"Error copying file {source_path}: {e}")
                        
class Import:
    def __init__(self):      
        if not os.path.exists("{}/.config".format(home)):
            os.system(f"mkdir {home}/.config/")
        print("importing settings from the Dconf database")
        if os.path.exists("user"):
            os.system(f"cp -R ./user {home}/.config/dconf/")
        else:
            if flatpak:
                os.system("dconf load / < ./dconf-settings.ini")
            else:
                os.system("echo user-db:user > temporary-profile")
                os.system('DCONF_PROFILE="$(pwd)/temporary-profile" dconf load / < dconf-settings.ini')
        print("importing list of installed Flatpak apps (them will be installed after the next login)")
        os.system(f'cp ./installed_flatpaks.sh {DATA}/')
        os.system(f'cp ./installed_user_flatpaks.sh {DATA}/')
        print("importing icons")
        os.system(f'cp -au ./icons {home}/.local/share/')
        os.system(f'cp -au ./.icons {home}/')
        print("importing themes")
        os.system(f'cp -au ./.themes {home}/')
        os.system(f'cp -au ./themes {home}/.local/share/')
        print("importing backgrounds")
        os.system(f'cp -au ./backgrounds {home}/.local/share/')
        print("importing fonts")
        os.system(f'cp -au ./.fonts {home}/')
        os.system(f'cp -au ./fonts {home}/.local/share/')
        print("importing Gtk settings")
        os.system(f'cp -au ./gtk-4.0 {home}/.config/')
        os.system(f'cp -au ./gtk-3.0 {home}/.config/')
        print("importing desktop directory")
        os.system(f'cp -au ./Desktop/* {GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)}/')
        # create this file to prevent removing the cache directory during importing configuration
        if os.path.exists(f'{CACHE}/import_config/app'):
            with open(f"copying_flatpak_data", "w") as c:
                c.write("copying flatpak data ...")
        elif os.path.exists(f'{CACHE}/syncing/app'):
            with open(f"copying_flatpak_data", "w") as c:
                c.write("copying flatpak data ...")
        print("importing desktop environment configuration files")
        # Apply configs for individual desktop environments
        if environment == 'GNOME':
            os.system(f'cp -au ./gnome-background-properties {home}/.local/share/')
            os.system(f'cp -au ./gnome-shell {home}/.local/share/')
            os.system(f'cp -au ./nautilus-python {home}/.local/share/')
            os.system(f'cp -au ./nautilus {home}/.local/share/')
            os.system(f'cp -au ./gnome-control-center {home}/.config/')
        elif environment == 'Pantheon':
            os.system(f'cp -au ./plank {home}/.config/')
            os.system(f'cp -au ./marlin {home}/.config/')
        elif environment == 'Cinnamon':
            os.system(f'cp -au ./nemo {home}/.config/')
            os.system(f'cp -au ./cinnamon {home}/.local/share/')
            os.system(f'cp -au ./.cinnamon {home}/')
        elif environment == 'Budgie':
            os.system(f'cp -au ./budgie-desktop {home}/.config/')
            os.system(f'cp -au ./budgie-extras {home}/.config/')
            os.system(f'cp -au ./nemo {home}/.config/')
        elif environment == 'COSMIC (Old)':
            os.system(f'cp -au ./pop-shell {home}/.config/')
            os.system(f'cp -au ./gnome-shell {home}/.local/share/')
        elif environment == 'COSMIC (New)':
            os.system(f"cp -au ./cosmic {home}/.config/")
            os.system(f"cp -au ./cosmic-state {home}/.local/state/cosmic")
        elif environment == 'Xfce':
            os.system(f'cp -au ./xfce4 {home}/.config/')
            os.system(f'cp -au ./Thunar {home}/.config/')
            os.system(f'cp -au ./.xfce4 {home}/')
        elif environment == 'MATE':
            os.system(f'cp -au ./caja {home}/.config/')
        elif environment == 'KDE Plasma':
            if os.path.exists(f"{CACHE}/syncing"):
                os.chdir("%s/syncing" % CACHE)
            else:
                os.chdir("%s/import_config" % CACHE)
            os.chdir('xdg-config')
            os.system(f'cp -au ./ {home}/.config/')
            if os.path.exists(f"{CACHE}/syncing"):
                os.chdir("%s/syncing" % CACHE)
            else:
                os.chdir("%s/import_config" % CACHE)
            os.chdir('xdg-data')
            os.system(f'cp -au ./ {home}/.local/share/')
        elif environment == 'Deepin':
            os.system(f"cp -au ./deepin {home}/.config/")
            os.system(f"cp -au ./deepin-data {home}/.local/share/deepin/")
        elif environment == None:
            print("→ SKIPPING: SaveDesktop is running in the TTY mode")
            
        if flatpak:
            self.create_flatpak_desktop()
        os.system(f"echo > {CACHE}/import_config/done")
        print("THE CONFIGURATION HAS BEEN IMPORTED SUCCESSFULLY!")
            
    # Create desktop file for install Flatpaks from list
    def create_flatpak_desktop(self):
        os.system(f"cp {system_dir}/install_flatpak_from_script.py {DATA}/")
        if not os.path.exists(f"{home}/.config/autostart"):
            os.mkdir(f"{home}/.config/autostart")
        if not os.path.exists(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"):
            with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as fa:
                fa.write(f"[Desktop Entry]\nName=SaveDesktop (Flatpak Apps installer)\nType=Application\nExec=python3 {DATA}/install_flatpak_from_script.py")
        
if args.save:
    Save()
elif args.import_:
    Import()
