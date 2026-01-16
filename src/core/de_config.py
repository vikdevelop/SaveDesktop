import os, shutil, subprocess
from gi.repository import GLib
from savedesktop.globals import *
from pathlib import Path

# ------------------------
# Helpers
# ------------------------

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

def safe_copytree(src: str, dst: str):
    if os.path.isdir(src):
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True, symlinks=True)
            print(f"[OK] Copied dir: {src} → {dst}")
        except Exception as e:
            print(f"[ERR] Dir copy failed {src} → {dst}: {e}")
    else:
        print(f"[SKIP] Directory not found: {src}")

# ------------------------
# Special handlers
# ------------------------

def save_icons():
    xdg_path = f"{home}/.local/share"
    legacy_path = f"{home}"

    if os.path.isdir(f"{xdg_path}/icons"):
        subprocess.run(["tar", "-czf", "icon-themes.tgz", "-C", xdg_path, "icons"])

    if os.path.isdir(f"{legacy_path}/.icons"):
        subprocess.run(["tar", "-czf", "icon-themes-legacy.tgz", "-C", legacy_path, ".icons"])

    print("[OK] Saving icons")

def import_icons():
    if os.path.exists("icon-themes.tgz"):
        subprocess.run(["tar", "-xzf", "icon-themes.tgz", "-C", f"{home}/.local/share"])

    if os.path.exists("icon-themes-legacy.tgz"):
        subprocess.run(["tar", "-xzf", "icon-themes-legacy.tgz", "-C", home])

    print("[OK] Importing icons")

def save_flatpak_data():
    blacklist = settings["disabled-flatpak-apps-data"]

    cmd = ["tar", "-czf", "flatpak-apps-data.tgz", "--exclude=*/cache"]

    for app in blacklist:
        cmd.append(f"--exclude={app}")

    cmd.extend(["-C", f"{home}/.var", "app"])

    subprocess.run(cmd)
    print("[OK] Saving Flatpak app data")

def create_flatpak_list():
    os.system("ls /var/lib/flatpak/app/ | awk '{print \"flatpak install --system \" $1 \" -y\"}' > installed_flatpaks.sh")
    os.system("ls ~/.local/share/flatpak/app | awk '{print \"flatpak install --user \" $1 \" -y\"}' > installed_user_flatpaks.sh")
    print("[OK] Saving Flatpak app list")

def create_flatpak_autostart():
    os.system(f"cp /app/share/savedesktop/savedesktop/core/flatpaks_installer.py {CACHE}/workspace")
    os.makedirs(f"{home}/.config/autostart", exist_ok=True)
    if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh"):
        with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as f:
            f.write(
                "[Desktop Entry]\n"
                "Name=SaveDesktop (Flatpak Apps installer)\n"
                "Type=Application\n"
                f"Exec=python3 {CACHE}/workspace/flatpaks_installer.py\n"
            )

    print("[OK] Created Flatpak autostart")

# ------------------------
# Desktop folder
# ------------------------

desktop_dir = Path(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP))

def save_desktop_folder():
    subprocess.run([
        "tar", "-czf", "desktop-folder.tgz",
        "-C", str(desktop_dir.parent),
        desktop_dir.name
    ])

    safe_copytree(f"{home}/.local/share/gvfs-metadata", "gvfs-metadata")
    print("[OK] Saving Desktop folder")

def import_desktop_folder():
    if os.path.exists("desktop-folder.tgz"):
        subprocess.run([
            "tar", "-xzf", "desktop-folder.tgz",
            "-C", str(desktop_dir.parent)
        ])
        print("[OK] Restored Desktop folder")

# ------------------------
# GENERAL ITEMS (DATA MODEL)
# ------------------------

GENERAL_ITEMS = {

    "fonts": {
        "key": "save-fonts",
        "dirs": [
            (f"{home}/.fonts", ".fonts"),
            (f"{home}/.local/share/fonts", "fonts"),
        ],
    },

    "themes": {
        "key": "save-themes",
        "dirs": [
            (f"{home}/.themes", ".themes"),
            (f"{home}/.local/share/themes", "themes"),
        ],
    },

    "gtk": {
        "key": "save-gtk-settings",
        "dirs": [
            (f"{home}/.config/gtk-4.0", "gtk-4.0"),
            (f"{home}/.config/gtk-3.0", "gtk-3.0"),
        ],
    },

    "backgrounds": {
        "key": "save-backgrounds",
        "dirs": [
            (f"{home}/.local/share/backgrounds", "backgrounds"),
            (f"{home}/.local/share/wallpapers", "wallpapers"),
        ],
    },

    "extensions": {
        "key": "save-extensions",
        "dirs": [
            (f"{home}/.local/share/gnome-shell", "gnome-shell"),
            (f"{home}/.local/share/cinnamon", "cinnamon"),
            (f"{home}/.local/share/plasma", "plasma"),
        ],
    },

}

# ------------------------
# SPECIAL ITEMS (CUSTOM LOGIC)
# ------------------------

SPECIAL_ITEMS = {

    "icons": {
        "key": "save-icons",
        "save": save_icons,
        "import": import_icons,
    },

    "flatpaks": {
        "key": "save-installed-flatpaks",
        "save": create_flatpak_list,
        "import": create_flatpak_autostart,
    },

    "flatpak-data": {
        "key": "save-flatpak-data",
        "save": save_flatpak_data,
        "import": create_flatpak_autostart,
    },

    "desktop": {
        "key": "save-desktop-folder",
        "save": save_desktop_folder,
        "import": import_desktop_folder,
    },

}

# Directories for KDE Plasma DE
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

# ------------------------
# Save pipeline
# ------------------------

class Save:

    def __init__(self):

        # General dirs
        for item in GENERAL_ITEMS.values():

            if settings[item["key"]]:

                for src, dst in item["dirs"]:
                    safe_copytree(src, dst)

        # Special handlers
        for item in SPECIAL_ITEMS.values():

            if settings[item["key"]]:
                item["save"]()

        # DE configuration
        if environment:
            if environment["de_name"] == "KDE Plasma":
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
            else:
                print(f"Saving environment-specific config for: {environment['de_name']}")
                for src, dst in environment["dirs"]:
                    safe_copytree(src, dst)
        else:
            print(f"[WARN] Unknown DE: {environment_key}")

        self.save_dconf()

    def save_dconf(self):
        os.system("dconf dump / > dconf-settings.ini")
        print("[OK] Saved dconf")

# ------------------------
# Import pipeline
# ------------------------

class Import:

    def __init__(self):

        # General dirs (reverse copy)
        for item in GENERAL_ITEMS.values():

            if settings[item["key"]]:

                for src, dst in item["dirs"]:
                    safe_copytree(dst, src)

        # Special handlers
        for item in SPECIAL_ITEMS.values():

            if settings[item["key"]]:
                item["import"]()

        # DE configuration
        if environment:
            if environment["de_name"] == "KDE Plasma":
                print("Importing KDE Plasma configuration...")
                for src, dst in KDE_DIRS_IMPORT:
                    safe_copytree(src, dst)
            else:
                print(f"Importing environment-specific config for: {environment['de_name']}")
                for src, dst in environment["dirs"]:
                    safe_copytree(dst, src)
        else:
            print(f"[WARN] Unknown DE: {environment_key}")

        self.import_dconf()

    def import_dconf(self):
        if flatpak:
            os.system("dconf load / < dconf-settings.ini")
        else:
            os.system("echo user-db:user > temporary-profile")
            os.system('DCONF_PROFILE="$(pwd)/temporary-profile" dconf load / < dconf-settings.ini')

        print("[OK] Imported dconf")
