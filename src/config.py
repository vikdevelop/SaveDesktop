import os, json, gi, argparse, shutil, psutil
from gi.repository import GLib, Gio
from localization import _, CACHE, DATA, home, system_dir, flatpak, snap, settings

# add command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save", help="Save the current configuration", action="store_true")
parser.add_argument("-i", "--import_", help="Import saved configuration", action="store_true")

#get all system processes
args = parser.parse_args()
processes = psutil.process_iter()

#initialize a var
packages = []

#creating a lambda functin to get the path to the package config folder
pathto=lambda package:os.getenv("HOME")+'.config/'+package+"/"

#a list of available packages for a wayland windowmanager
available_packages = ["waybar","swaybg","wpaperd","mpvpaper","swww","waypaper","eww"]

#getting only the names of the processes
names = [x.name for x in processes]

#selecting the found packages and appending them to the package list
for name in names:
    for package in available_packages:
        if package in name:
            packages.append(pathto(package))
            
# check of the user's current DE
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
elif os.getenv('XDG_CURRENT_DESKTOP') == 'Hyprland':
    environment = 'Hyprland'
else:
    from tty_environments import *

class Save:
    def __init__(self):
        # create a txt file to prevent deleting the current saving by closing the application window
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
        elif environment == 'Hyprland':
    
    # save Flatpak apps data
    def save_flatpak_data(self):
        blst = settings["disabled-flatpak-apps-data"]
        # convert GSettings property to a list
        blacklist = blst
        
        # set destination dir
        if os.path.exists(f"{CACHE}/periodic_saving/saving_status"):
            os.makedirs(f"{CACHE}/periodic_saving/app", exist_ok=True)
            destdir = f"{CACHE}/periodic_saving/app"
        else:
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
            
    # Create desktop file for install Flatpaks from a list
    def create_flatpak_desktop(self):
        os.system(f"cp {system_dir}/install_flatpak_from_script.py {DATA}/")
        if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh") or not os.path.exists(f"{CACHE}/syncing/sync_status"):
            if not os.path.exists(f"{home}/.config/autostart"):
                os.mkdir(f"{home}/.config/autostart")
            if not os.path.exists(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"):
                with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as fa:
                    fa.write(f"[Desktop Entry]\nName=SaveDesktop (Flatpak Apps installer)\nType=Application\nExec=python3 {DATA}/install_flatpak_from_script.py")

if args.save:
    Save()
elif args.import_:
    Import()
