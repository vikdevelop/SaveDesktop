import os
import json
import gi
from gi.repository import GLib, Gio
from localization import _, CACHE, DATA, home, system_dir, flatpak, snap
import argparse

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
    
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
cache_replacing = f'{CACHE}'
config = cache_replacing.replace("cache/tmp", "config/glib-2.0/settings")

class Save:
    def __init__(self):
        os.system("dconf dump / > ./dconf-settings.ini")
        #os.system('cp -R {home}/.config/dconf/user ./')
        os.system(f'cp -R {home}/.config/gtk-4.0 ./')
        os.system(f'cp -R {home}/.config/gtk-3.0 ./')
        if settings["save-backgrounds"] == True:
            os.system(f'cp -R {home}/.local/share/backgrounds ./')
        if settings["save-icons"] == True:
            os.system(f'cp -R {home}/.local/share/icons ./')
            os.system(f'cp -R {home}/.icons ./')
        if settings["save-themes"] == True:
            os.system(f'cp -R {home}/.themes ./')
        if settings["save-fonts"] == True:
            os.system(f'cp -R {home}/.fonts ./')
        if settings["save-installed-flatpaks"] == True:
            os.system('sh /app/backup_flatpaks.sh')
        if settings["save-flatpak-data"] == True:
            os.system(f'cp -R {home}/.var/app ./')
            
        # Save configs on individual desktop environments
        if environment == 'GNOME':
            os.system(f"cp -R {home}/.local/share/gnome-background-properties ./")
            os.system(f"cp -R {home}/.local/share/gnome-shell ./")
            os.system(f"cp -R {home}/.local/share/nautilus-python ./")
            os.system(f"cp -R {home}/.local/share/nautilus ./")
            os.system(f"cp -R {home}/.config/gnome-control-center ./")
        elif environment == 'Pantheon':
            os.system(f"cp -R {home}/.config/plank ./")
            os.system(f"cp -R {home}/.config/marlin ./")
        elif environment == 'Cinnamon':
            os.system(f"cp -R {home}/.config/nemo ./")
            os.system(f"cp -R {home}/.local/share/cinnamon ./")
            os.system(f"cp -R {home}/.cinnamon ./")
        elif environment == 'Budgie':
            os.system(f"cp -R {home}/.config/budgie-desktop ./")
            os.system(f"cp -R {home}/.config/budgie-extras ./")
            os.system(f"cp -R {home}/.config/nemo ./")
        elif environment == 'COSMIC':
            os.system(f"cp -R {home}/.config/pop-shell ./")
            os.system(f"cp -R {home}/.local/share/gnome-shell ./")
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
            os.system(f"cp -R {home}/.local/share/[k]* ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/dolphin ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/sddm ./xdg-data/")
            if settings["save-backgrounds"] == True:
                os.system(f"cp -R {home}/.local/share/wallpapers ./xdg-data/")
            os.system(f"cp -R {home}/.local/share/plasma-systemmonitor ./xdg-data/")
        os.system(f"tar --gzip -cf cfg.sd.tar.gz ./")
        if os.path.exists(f"{CACHE}/.filedialog.json"):
            with open(f"{CACHE}/.filedialog.json") as j:
                j = json.load(j)
        elif os.path.exists(f"{CACHE}/.periodicfile.json"):
            with open(f"{CACHE}/.periodicfile.json") as j:
                j = json.load(j)
        os.system(f"mv ./cfg.sd.tar.gz {j['recent_file']}")
        
class Import:
    def __init__(self):
        if os.path.exists(f"{CACHE}/.impfile.json"):
            with open(f"{CACHE}/.impfile.json") as j:
                j = json.load(j)
            os.system("tar -xf %s ./" % j["import_file"])
        if not os.path.exists("{}/.config".format(home)):
            os.system(f"mkdir {home}/.config/")
        if os.path.exists("user"):
            os.system(f"cp -R ./user {home}/.config/dconf/")
        else:
            if flatpak:
                os.system("dconf load / < ./dconf-settings.ini")
            else:
                os.system("echo user-db:user > temporary-profile")
                os.system('DCONF_PROFILE="$(pwd)/temporary-profile" dconf load / < dconf-settings.ini')
        os.system(f'cp -R ./icons {home}/.local/share/')
        os.system(f'cp -R ./.themes {home}/')
        os.system(f'cp -R ./.icons {home}/')
        os.system(f'cp -R ./backgrounds {home}/.local/share/')
        os.system(f'cp -R ./.fonts {home}/')
        os.system(f'cp -R ./gtk-4.0 {home}/.config/')
        os.system(f'cp -R ./gtk-3.0 {home}/.config/')
        os.system(f'cp -R ./app {home}/.var/')
        os.system(f'cp -R ./savedesktop-user-settings.ini {config}/keyfile')
        os.system(f'cp ./installed_flatpaks.sh {DATA}/')
        # Apply configs for individual desktop environments
        if environment == 'GNOME':
            os.system(f'cp -R ./gnome-background-properties {home}/.local/share/')
            os.system(f'cp -R ./gnome-shell {home}/.local/share/')
            os.system(f'cp -R ./nautilus-python {home}/.local/share/')
            os.system(f'cp -R ./gnome-control-center {home}/.config/')
        elif environment == 'Pantheon':
            os.system(f'cp -R ./plank {home}/.config/')
            os.system(f'cp -R ./marlin {home}/.config/')
        elif environment == 'Cinnamon':
            os.system(f'cp -R ./nemo {home}/.config/')
            os.system(f'cp -R ./cinnamon {home}/.local/share/')
            os.system(f'cp -R ./.cinnamon {home}/')
        elif environment == 'Budgie':
            os.system(f'cp -R ./budgie-desktop {home}/.config/')
            os.system(f'cp -R ./budgie-extras {home}/.config/')
            os.system(f'cp -R ./nemo {home}/.config/')
        elif environment == 'COSMIC':
            os.system(f'cp -R ./pop-shell {home}/.config/')
            os.system(f'cp -R ./gnome-shell {home}/.local/share/')
        elif environment == 'Xfce':
            os.system(f'cp -R ./xfce4 {home}/.config/')
            os.system(f'cp -R ./Thunar {home}/.config/')
            os.system(f'cp -R ./.xfce4 {home}/')
        elif environment == 'MATE':
            os.system(f'cp -R ./caja {home}/.config/')
        elif environment == 'KDE Plasma':
            os.chdir("%s/syncing" % CACHE)
            os.chdir('xdg-config')
            os.system(f'cp -R ./ {home}/.config/')
            os.chdir("%s/syncing" % CACHE)
            os.chdir('xdg-data')
            os.system(f'cp -R ./ {home}/.local/share/')
        if not snap:
            self.create_flatpak_desktop()
            
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
