import os, shutil, argparse
from gi.repository import GLib
from savedesktop.globals import *

# Helping functions
def safe_copy(src: str, dst: str):
    if os.path.isfile(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            shutil.copy2(src, dst)
            print(f"[OK] Copied file: {src} → {dst}")
        except Exception as e:
            print(f"[ERR] File copy failed {src} → {dst}: {e}")
    else:
        print(f"[SKIP] File not found: {src}")

def safe_copytree(src: str, dst: str, ignore=None):
    if os.path.isdir(src):
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)
            print(f"[OK] Copied dir: {src} → {dst}")
        except Exception as e:
            print(f"[ERR] Dir copy failed {src} → {dst}: {e}")
    else:
        print(f"[SKIP] Directory not found: {src}")

# Desktop environments list and their directories
GNOME_DIRS = [
    (f"{home}/.local/share/gnome-background-properties", "gnome-background-properties"),
    (f"{home}/.local/share/nautilus-python", "nautilus-python"),
    (f"{home}/.local/share/nautilus", "nautilus"),
    (f"{home}/.config/gnome-control-center", "gnome-control-center"),
]

ENVIRONMENTS = {
    "GNOME": {"de_name": "GNOME", "dirs": GNOME_DIRS},
    "ubuntu:GNOME": {"de_name": "GNOME", "dirs": GNOME_DIRS},
    "zorin:GNOME": {"de_name": "GNOME", "dirs": GNOME_DIRS},
    "Pantheon": {"de_name": "Pantheon", "dirs": [(f"{home}/.config/plank", "plank"), (f"{home}/.config/marlin", "marlin")]},
    "Cinnamon": {"de_name": "Cinnamon", "dirs": [(f"{home}/.config/nemo", "nemo"), (f"{home}/.local/share/cinnamon", "cinnamon"), (f"{home}/.cinnamon", ".cinnamon")]},
    "Budgie:GNOME": {"de_name": "Budgie", "dirs": [(f"{home}/.config/budgie-desktop", "budgie-desktop"), (f"{home}/.config/budgie-extras", "budgie-extras"), (f"{home}/.config/nemo", "nemo")]},
    "pop:GNOME": {"de_name": "COSMIC (Old)", "dirs": [(f"{home}/.config/pop-shell", "pop-shell"), (f"{home}/.local/share/nautilus", "nautilus")]},
    "COSMIC": {"de_name": "COSMIC (New)", "dirs": [(f"{home}/.config/cosmic", "cosmic"), (f"{home}/.local/state/cosmic", "cosmic-state")]},
    "XFCE": {"de_name": "Xfce", "dirs": [(f"{home}/.config/xfce4", "xfce4"), (f"{home}/.config/Thunar", "Thunar"), (f"{home}/.xfce4", ".xfce4")]},
    "MATE": {"de_name": "MATE", "dirs": [(f"{home}/.config/caja", "caja")]},
    "Deepin": {"de_name": "Deepin", "dirs": [(f"{home}/.config/deepin", "deepin"), (f"{home}/.local/share/deepin", "deepin-data")]},
    "Hyprland": {"de_name": "Hyprland", "dirs": [(f"{home}/.config/hypr", "hypr")]},
}

KDE_DIRS_SAVE = [
    (f"{home}/.config/plasmarc", "xdg-config/plasmarc"),
    (f"{home}/.config/plasmashellrc", "xdg-config/plasmashellrc"),
    (f"{home}/.config/plasma-org.kde.plasma.desktop-appletsrc", "xdg-config/plasma-org.kde.plasma.desktop-appletsrc"),
    (f"{home}/.config/dolphinrc", "xdg-config/dolphinrc"),
    (f"{home}/.config/gtkrc", "xdg-config/gtkrc"),
    (f"{home}/.config/Kvantum", "xdg-config/Kvantum"),
    (f"{home}/.config/latte", "xdg-config/latte"),
    (f"{home}/.local/share/dolphin", "xdg-data/dolphin"),
    (f"{home}/.local/share/sddm", "xdg-data/sddm"),
    (f"{home}/.local/share/aurorae", "xdg-data/aurorae"),
    (f"{home}/.local/share/plasma-systemmonitor", "xdg-data/plasma-systemmonitor"),
    (f"{home}/.local/share/color-schemes", "xdg-data/color-schemes"),
]

KDE_DIRS_IMPORT = [
    ("xdg-config", f"{home}/.config"),
    ("xdg-data", f"{home}/.local/share"),
]

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save", help="Save the current configuration", action="store_true")
parser.add_argument("-i", "--import_", help="Import saved configuration", action="store_true")
args = parser.parse_args()

XDG = os.getenv("XDG_CURRENT_DESKTOP", "")
environment_key = XDG
environment = ENVIRONMENTS.get(environment_key, None)


class Save:
    def __init__(self):
        
        # Dconf
        print("Saving settings from the Dconf database...")
        os.system("dconf dump / > ./dconf-settings.ini")

        # GTK configs
        safe_copytree(f"{home}/.config/gtk-4.0", "gtk-4.0")
        safe_copytree(f"{home}/.config/gtk-3.0", "gtk-3.0")

        # Fonts, themes, extensions, backgrounds, icons
        if settings["save-fonts"]:
            safe_copytree(f"{home}/.fonts", ".fonts")
            safe_copytree(f"{home}/.local/share/fonts", "fonts")
        if settings["save-themes"]:
            safe_copytree(f"{home}/.themes", ".themes")
            safe_copytree(f"{home}/.local/share/themes", "themes")
        if settings["save-extensions"]:
            safe_copytree(f"{home}/.local/share/gnome-shell", "gnome-shell")
            safe_copytree(f"{home}/.local/share/cinnamon", "cinnamon")
            safe_copytree(f"{home}/.local/share/plasma", "xdg-data/plasma")
        if settings["save-backgrounds"]:
            safe_copytree(f"{home}/.local/share/backgrounds", "backgrounds")
            safe_copytree(f"{home}/.local/share/wallpapers", "xdg-data/wallpapers")
        if settings["save-icons"]:
            safe_copytree(f"{home}/.icons", ".icons")
            safe_copytree(f"{home}/.local/share/icons", "icons")

        # Desktop folder
        if settings["save-desktop-folder"]:
            desktop_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP)
            if desktop_dir:
                safe_copytree(desktop_dir, "Desktop")
            safe_copytree(f"{home}/.local/share/gvfs-metadata", "gvfs-metadata")
        
        # Flatpak apps and their data
        if flatpak:
            if settings["save-installed-flatpaks"]:
                print("saving list of installed Flatpak apps")
                os.system("ls /var/lib/flatpak/app/ | awk '{print \"flatpak install --system \" $1 \" -y\"}' > ./installed_flatpaks.sh")
                os.system("ls ~/.local/share/flatpak/app | awk '{print \"flatpak install --user \" $1 \" -y\"}' > ./installed_user_flatpaks.sh")
            if settings["save-flatpak-data"]:
                print("saving user data of installed Flatpak apps")
                self.save_flatpak_data()

        # Environment specific
        if environment_key == "KDE":
            print("Saving KDE Plasma configuration...")
            os.makedirs("xdg-config", exist_ok=True)
            os.makedirs("xdg-data", exist_ok=True)
            os.system(f"cp -R {home}/.config/[k]* ./xdg-config/")
            os.system(f"cp -R {home}/.local/share/[k]* ./xdg-data/")
            for src, dst in KDE_DIRS_SAVE:
                if os.path.isfile(src):
                    safe_copy(src, dst)
                else:
                    safe_copytree(src, dst)
        elif environment:
            print(f"Saving environment-specific config for: {environment['de_name']}")
            for src, dst in environment["dirs"]:
                safe_copytree(src, dst)
        else:
            print(f"[WARN] Unknown DE: {environment_key}")
    
    # Save the Flatpak apps' data
    def save_flatpak_data(self):
        gsettings = settings["disabled-flatpak-apps-data"]
        black_list = gsettings # convert GSettings property to a list
        
        # set destination dir
        if os.path.exists(f"{CACHE}/periodic_saving/saving_status"):
            os.makedirs(f"{CACHE}/periodic_saving/app", exist_ok=True)
            destdir = f"{CACHE}/periodic_saving/app"
        else:
            os.makedirs(f"{CACHE}/save_config/app", exist_ok=True)
            destdir = f"{CACHE}/save_config/app"
        
        # copy Flatpak apps data
        for item in os.listdir(f"{home}/.var/app"):
            if item not in black_list and item != "cache":
                source_path = os.path.join(f"{home}/.var/app", item)
                destination_path = os.path.join(destdir, item)
                if os.path.isdir(source_path):
                    try:
                        shutil.copytree(source_path, destination_path, ignore=shutil.ignore_patterns('cache'))
                    except Exception as e:
                        print(f"Error copying directory {source_path}: {e}")
                else:
                    try:
                        shutil.copy2(source_path, destination_path)
                    except Exception as e:
                        print(f"Error copying file {source_path}: {e}")

class Import:
    def __init__(self):
        print("Importing settings...")
        
        # Dconf
        if flatpak:
            os.system("dconf load / < ./dconf-settings.ini")
        else:
            os.system("echo user-db:user > temporary-profile")
            os.system('DCONF_PROFILE="$(pwd)/temporary-profile" dconf load / < dconf-settings.ini')

        # Fonts, Themes, GTK, Extensions, Desktop folder, Backgrounds, Icons
        safe_copytree("fonts", f"{home}/.local/share/fonts")
        safe_copytree(".fonts", f"{home}/.fonts")
        safe_copytree("themes", f"{home}/.local/share/themes")
        safe_copytree(".themes", f"{home}/.themes")
        safe_copytree("gtk-4.0", f"{home}/.config/gtk-4.0")
        safe_copytree("gtk-3.0", f"{home}/.config/gtk-3.0")
        safe_copytree("gnome-shell", f"{home}/.local/share/gnome-shell")
        safe_copytree("cinnamon", f"{home}/.local/share/cinnamon")
        safe_copytree("plasma", f"{home}/.local/share/plasma")
        safe_copytree("Desktop", GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP))
        safe_copytree("gvfs-metadata", f"{home}/.local/share/gvfs-metadata")
        safe_copytree("backgrounds", f"{home}/.local/share/backgrounds")
        safe_copytree("wallpapers", f"{home}/.local/share/wallpapers")
        safe_copytree("icons", f"{home}/.local/share/icons")
        safe_copytree(".icons", f"{home}/.icons")

        # Environment specific
        if environment_key == "KDE":
            print("Importing KDE Plasma configuration...")
            for src, dst in KDE_DIRS_IMPORT:
                safe_copytree(src, dst)
        elif environment:
            print(f"Importing environment-specific config for: {environment['de_name']}")
            for src, dst in environment["dirs"]:
                safe_copytree(dst, src)
        else:
            print(f"[WARN] Unknown DE: {environment_key}")
        
        if flatpak: 
            if any(os.path.exists(path) for path in ["app", "installed_flatpaks.sh", "installed_user_flatpaks.sh"]): 
                self.create_flatpak_autostart()
    
    # Create an autostart file to install Flatpaks from a list after the next login 
    def create_flatpak_autostart(self):
        os.system(f"cp /app/share/savedesktop/savedesktop/core/flatpaks_installer.py {CACHE}/")
        if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh") or not os.path.exists(f"{CACHE}/syncing/sync_status"):
            if not os.path.exists(f"{home}/.config/autostart"): 
                os.mkdir(f"{home}/.config/autostart")
            if not os.path.exists(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"):
                with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as fa:
                    fa.write(f"[Desktop Entry]\nName=SaveDesktop (Flatpak Apps installer)\nType=Application\nExec=python3 {CACHE}/flatpaks_installer.py")

if args.save:
    Save()
elif args.import_:
    Import()
