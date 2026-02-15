import os, shutil, subprocess, json
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
        subprocess.run(["tar", "-czf", "General/icon-themes.tgz", "-C", xdg_path, "icons"])

    if os.path.isdir(f"{legacy_path}/.icons"):
        subprocess.run(["tar", "-czf", "General/icon-themes-legacy.tgz", "-C", legacy_path, ".icons"])

    print("[OK] Saving icons")

def import_icons():
    if os.path.exists("General"):
        if os.path.exists("General/icon-themes.tgz"):
            subprocess.run(["tar", "-xzf", "General/icon-themes.tgz", "-C", f"{home}/.local/share"])

        if os.path.exists("General/icon-themes-legacy.tgz"):
            subprocess.run(["tar", "-xzf", "General/icon-themes-legacy.tgz", "-C", home])

        print("[OK] Importing icons")
    else:
        if os.path.exists("icon-themes.tgz"):
            subprocess.run(["tar", "-xzf", "icon-themes.tgz", "-C", f"{home}/.local/share"])

        if os.path.exists("icon-themes-legacy.tgz"):
            subprocess.run(["tar", "-xzf", "icon-themes-legacy.tgz", "-C", home])

        print("[OK] Importing icons")

def save_flatpak_data():
    blacklist = settings["disabled-flatpak-apps-data"]

    cmd = ["tar", "-czf", "Flatpak_Apps/flatpak-apps-data.tgz", "--exclude=*/cache"]

    for app in blacklist:
        cmd.append(f"--exclude={app}")

    cmd.extend(["-C", f"{home}/.var", "app"])

    subprocess.run(cmd)
    print("[OK] Saving Flatpak app data")

def export_flatpaks(path, output_file, install_type):
    if os.path.exists(path):
        apps = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        with open(output_file, 'w') as f:
            for app in apps:
                if not app in settings["disabled-flatpak-apps-data"]:
                    f.write(f"flatpak install --{install_type} {app} -y\n")

def create_flatpak_list():
    export_flatpaks('/var/lib/flatpak/app/', 'Flatpak_Apps/installed_flatpaks.sh', 'system')
    export_flatpaks(f'{home}/.local/share/flatpak/app', 'Flatpak_Apps/installed_user_flatpaks.sh', 'user')
    print("[OK] Saving Flatpak app list")

def create_flatpak_autostart():
    os.system(f"cp /app/share/savedesktop/savedesktop/core/flatpaks_installer.py {CACHE}/workspace")

    # Create a JSON file with the user's preferences for Flatpak apps
    with open(f"{CACHE}/workspace/flatpak-prefs.json", "w") as fl:
        json.dump({"keep-flatpaks": settings["keep-flatpaks"], "disabled-flatpaks": settings["disabled-flatpak-apps-data"], "install-flatpaks": settings["save-installed-flatpaks"], "copy-data": settings["save-flatpak-data"]}, fl)

    # Create an autostart file for post-login Flatpak installation
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

def save_bookmarks():
    safe_copytree(f"{home}/.config/gtk-4.0", "General/gtk-4.0")
    if settings["save-bookmarks"]:
        safe_copy(f"{home}/.config/gtk-3.0/bookmarks", "General/gtk-3.0/bookmarks")

def import_bookmarks():
    if os.path.exists("General"):
        safe_copytree("General/gtk-4.0", f"{home}/.config/gtk-4.0", )
        if settings["save-bookmarks"]:
            safe_copy("General/gtk-3.0/bookmarks", f"{home}/.config/gtk-3.0/bookmarks")
    else:
        safe_copytree("gtk-4.0", f"{home}/.config/gtk-4.0", )
        if settings["save-bookmarks"]:
            safe_copy("gtk-3.0/bookmarks", f"{home}/.config/gtk-3.0/bookmarks")

# ------------------------
# Desktop folder
# ------------------------

desktop_dir = Path(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP))

def save_desktop_folder():
    subprocess.run([
        "tar", "-czf", "General/desktop-folder.tgz",
        "-C", str(desktop_dir.parent),
        desktop_dir.name
    ])

    safe_copytree(f"{home}/.local/share/gvfs-metadata", "General/gvfs-metadata")
    print("[OK] Saving Desktop folder")

def import_desktop_folder():
    if os.path.exists("General"):
        subprocess.run([
            "tar", "-xzf", "General/desktop-folder.tgz",
            "-C", str(desktop_dir.parent)
        ])
        safe_copytree("General/gvfs-metadata", f"{home}/.local/share/gvfs-metadata")
        print("[OK] Restored Desktop folder")
    else:
        subprocess.run([
            "tar", "-xzf", "desktop-folder.tgz",
            "-C", str(desktop_dir.parent)
        ])
        safe_copytree("gvfs-metadata", f"{home}/.local/share/gvfs-metadata")
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

    "bookmarks": {
        "key": "save-bookmarks",
        "save": save_bookmarks,
        "import": import_bookmarks,
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
        os.makedirs("General", exist_ok=True)
        os.makedirs("DE", exist_ok=True)
        os.makedirs("Flatpak_Apps", exist_ok=True)
        os.makedirs("Custom_Dirs", exist_ok=True)

        # General dirs
        for item in GENERAL_ITEMS.values():
            if settings[item["key"]]:
                for src, dst in item["dirs"]:
                    safe_copytree(src, os.path.join("General", dst))

        # Special handlers
        for item in SPECIAL_ITEMS.values():
            if settings[item["key"]]:
                item["save"]()

        # Custom dirs
        for folder in settings["custom-dirs"]:
            short_folder = Path(folder).relative_to(home)
            safe_copytree(folder, f"Custom_Dirs/{short_folder}")

        # DE configuration
        if environment:
            if environment["de_name"] == "KDE Plasma":
                print("Saving KDE Plasma configuration...")
                os.makedirs("DE/xdg-config", exist_ok=True)
                os.makedirs("DE/xdg-data", exist_ok=True)
                os.system(f"cp -R {home}/.config/[k]* ./DE/xdg-config/")
                os.system(f"cp -R {home}/.local/share/[k]* ./DE/xdg-data/")
                for src, dst in KDE_DIRS_SAVE:
                    if os.path.isfile(src):
                        safe_copy(src, os.path.join("DE", dst))
                    else:
                        safe_copytree(src, os.path.join("DE", dst))
            else:
                print(f"Saving environment-specific config for: {environment['de_name']}")
                for src, dst in environment["dirs"]:
                    safe_copytree(src, os.path.join("DE", dst))
        else:
            print(f"[WARN] Unknown DE: {environment_key}")

        self.save_dconf()

    def save_dconf(self):
        os.system("dconf dump / > ./General/dconf-settings.ini")
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
                    if os.path.exists("General"):
                        safe_copytree(os.path.join("General", dst), src)
                    else:
                        safe_copytree(dst, src)

        # Special handlers
        for item in SPECIAL_ITEMS.values():
            if settings[item["key"]]:
                item["import"]()

        # Custom dirs
        for folder in settings["custom-dirs"]:
            short_folder = Path(folder).relative_to(home)
            safe_copytree(f"Custom_Dirs/{short_folder}", folder)

        # DE configuration
        if environment:
            if environment["de_name"] == "KDE Plasma":
                print("Importing KDE Plasma configuration...")
                for src, dst in KDE_DIRS_IMPORT:
                    if os.path.exists("DE"):
                        safe_copytree(os.path.join("DE", src), dst)
                    else:
                        safe_copytree(src, dst)
            else:
                print(f"Importing environment-specific config for: {environment['de_name']}")
                for src, dst in environment["dirs"]:
                    if os.path.exists("DE"):
                        safe_copytree(os.path.join("DE", dst), src)
                    else:
                        safe_copytree(dst, src)
        else:
            print(f"[WARN] Unknown DE: {environment_key}")

        self.import_dconf()

    def import_dconf(self):
        if flatpak:
            if os.path.exists("General"):
                os.system("dconf load / < ./General/dconf-settings.ini")
            else:
                os.system("dconf load / < ./dconf-settings.ini")
        else:
            os.system("echo user-db:user > temporary-profile")

            if os.path.exists("General"):
                os.system('DCONF_PROFILE="$(pwd)/temporary-profile" dconf load / < ./General/dconf-settings.ini')
            else:
                os.system('DCONF_PROFILE="$(pwd)/temporary-profile" dconf load / < ./dconf-settings.ini')

        print("[OK] Imported dconf")
