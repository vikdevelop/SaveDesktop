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
            'home': Path(os.getenv('HOME', Path.home())),
            'run_cmd': 'flatpak run io.github.vikdevelop.SaveDesktop',
            'cache': f'{GLib.get_user_cache_dir()}/tmp',
            'data': f'{GLib.get_user_data_dir()}'
        }
    
    elif os.environ.get('SNAP_NAME') == 'savedesktop':
        return {
            'type': 'snap',
            'home': Path(os.getenv('SNAP_REAL_HOME', os.getenv('HOME', Path.home()))),
            'run_cmd': 'savedesktop',
            'cache': f'{GLib.get_user_cache_dir()}',
            'data': f'{GLib.get_user_data_dir()}'
        }
    
    else:
        return {
            'type': 'native',
            'home': Path.home(),
            'run_cmd': 'savedesktop',
            'cache': os.path.join(f'{GLib.get_user_cache_dir()}', 'io.github.vikdevelop.SaveDesktop'),
            'data': os.path.join(f'{GLib.get_user_data_dir()}', 'io.github.vikdevelop.SaveDesktop')
        }

env = get_app_environment()

home = env['home']

# System paths
download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
settings = Gio.Settings.new_with_path(
    "io.github.vikdevelop.SaveDesktop", 
    "/io/github/vikdevelop/SaveDesktop/"
)

# Cache and data directories
CACHE = env['cache']
DATA = env['data']

# Commands
periodic_saving_cmd = f'{env["run_cmd"]} --background'
sync_cmd = f'{env["run_cmd"]} --sync'

# Detect flags
flatpak = (env['type'] == 'flatpak')
snap = (env['type'] == 'snap')

# Application path
app_prefix = os.environ.get('SAVEDESKTOP_DIR')

# Export
__all__ = [
    'home', 'download_dir', 'snap', 'flatpak', 'settings',
    'DATA', 'CACHE', 'app_prefix', 'periodic_saving_cmd', 'sync_cmd'
]

