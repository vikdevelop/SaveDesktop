#!/usr/bin/env python3
import gi, os, locale, gettext
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from pathlib import Path

# Environment detection
def get_app_environment():
    if os.path.exists("/.flatpak-info"):
        return {
            'type': 'flatpak',
            'home': Path(os.getenv('HOME', Path.home())),
            'version_suffix': '',
            'run_cmd': 'flatpak run io.github.vikdevelop.SaveDesktop'
        }
    
    elif os.environ.get('SNAP_NAME') == 'savedesktop':
        return {
            'type': 'snap',
            'home': Path(os.getenv('SNAP_REAL_HOME', os.getenv('HOME', Path.home()))),
            'version_suffix': '-snap',
            'run_cmd': 'savedesktop'
        }
    
    else:
        return {
            'type': 'native',
            'home': Path.home(),
            'version_suffix': '-native', 
            'run_cmd': 'savedesktop'
        }

env = get_app_environment()

home = env['home']
version = f"1.0.0{env['version_suffix']}"

# System paths
download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
settings = Gio.Settings.new_with_path(
    "io.github.vikdevelop.SaveDesktop", 
    "/io/github/vikdevelop/SaveDesktop/"
)

DATA = f'{GLib.get_user_data_dir()}'
CACHE = f'{GLib.get_user_cache_dir()}'

# Commands
periodic_saving_cmd = f'{env["run_cmd"]} --background'
sync_cmd = f'{env["run_cmd"]} --sync'

# Detect flags
flatpak = (env['type'] == 'flatpak')
snap = (env['type'] == 'snap')

# Export
__all__ = [
    'home', 'download_dir', 'snap', 'flatpak', 'settings',
    'DATA', 'CACHE', 'version',
    'periodic_saving_cmd', 'sync_cmd'
]

