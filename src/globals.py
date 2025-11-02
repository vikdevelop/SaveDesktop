#!/usr/bin/env python3
import gi, os, locale
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from pathlib import Path

# Environment detection
def get_app_environment():
    if os.path.exists("/.flatpak-info"):
        return {
            'type': 'flatpak',
            'run_cmd': 'flatpak run io.github.vikdevelop.SaveDesktop',
            'cache': f'{GLib.get_user_cache_dir()}/tmp',
            'data': f'{GLib.get_user_data_dir()}'
        }
    
    else:
        return {
            'type': 'native',
            'run_cmd': 'savedesktop',
            'cache': os.path.join(f'{GLib.get_user_cache_dir()}', 'io.github.vikdevelop.SaveDesktop'),
            'data': os.path.join(f'{GLib.get_user_data_dir()}', 'io.github.vikdevelop.SaveDesktop')
        }

env = get_app_environment()

home = Path.home()

# System paths
download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
settings = Gio.Settings.new_with_path(
    "io.github.vikdevelop.SaveDesktop", 
    "/io/github/vikdevelop/SaveDesktop/"
)

# Cache and data directories
CACHE = env['cache']
DATA = env['data']

os.makedirs(CACHE, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

# Commands
periodic_saving_cmd = f'{env["run_cmd"]} --periodic-save'
sync_cmd = f'{env["run_cmd"]} --periodic-sync'

# Detect flags
flatpak = (env['type'] == 'flatpak')

# Application path
app_prefix = os.environ.get('SAVEDESKTOP_DIR')

# Desktop Environment Detection
# Desktop environments list and their directories
GNOME_DIRS = [
    (f"{home}/.local/share/gnome-background-properties", "gnome-background-properties"),
    (f"{home}/.local/share/nautilus-python", "nautilus-python"),
    (f"{home}/.local/share/nautilus", "nautilus"),
    (f"{home}/.config/gnome-control-center", "gnome-control-center"),
]

BUDGIE_DIRS = [
    (f"{home}/.config/budgie-desktop", "budgie-desktop"),
    (f"{home}/.config/budgie-extras", "budgie-extras"),
    (f"{home}/.config/nemo", "nemo")
]

ENVIRONMENTS = {
    "GNOME": {"de_name": "GNOME", "dirs": GNOME_DIRS},
    "ubuntu:GNOME": {"de_name": "GNOME", "dirs": GNOME_DIRS},
    "zorin:GNOME": {"de_name": "GNOME", "dirs": GNOME_DIRS},
    "Pantheon": {"de_name": "Pantheon", "dirs": [(f"{home}/.config/plank", "plank"), (f"{home}/.config/marlin", "marlin")]},
    "X-Cinnamon": {"de_name": "Cinnamon", "dirs": [(f"{home}/.config/nemo", "nemo"), (f"{home}/.local/share/cinnamon", "cinnamon"), (f"{home}/.cinnamon", ".cinnamon")]},
    "Budgie": {"de_name": "Budgie", "dirs": BUDGIE_DIRS},
    "Budgie:GNOME": {"de_name": "Budgie", "dirs": BUDGIE_DIRS},
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

XDG = os.getenv("XDG_CURRENT_DESKTOP", "")
environment = ENVIRONMENTS.get(XDG, None)

# Export
__all__ = [
    'home', 'download_dir', 'flatpak', 'settings', 'DATA', 'CACHE',
    'app_prefix', 'periodic_saving_cmd', 'sync_cmd', 'XDG', 'environment'
]

