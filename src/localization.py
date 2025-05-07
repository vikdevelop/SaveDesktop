#!/usr/bin/python3
import json, locale, os, socket, subprocess, gi
from pathlib import Path
from gi.repository import Gio, GLib

# For simpler import this script to the other scripts
__all__ = ['_', 'home', 'download_dir', 'snap', 'flatpak', 'settings', 'DATA', 'CACHE', 'r_lang', 'version', 'icon', 'rel_notes', 'system_dir', 'periodic_saving_cmd', 'sync_cmd']

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

# Set application version, and icon
v = "3.6_2"
icon = "io.github.vikdevelop.SaveDesktop"
rel_notes = "<p>Added support for saving a configuration without creating the archive and changed the archive format from *.tgz to *.tzst</p>\
<p>3.6_1-beta</p><ul>\
<li>Added an option to encrypt the periodic saving files and added support for its usage in the synchronization</li>\
<li>Changed the archive format from *.tar.gz to *.tgz (only for manual saving yet)</li>\
<li>Minor UI improvements</li>\
</ul>"

flatpak = os.path.exists("/.flatpak-info")
snap = os.environ.get('SNAP_NAME', '') == 'savedesktop'

# Checking for Snap and Real Home directories

snap_home = Path.home()#keeping this value if it comes handy
snap_real_home = os.getenv('SNAP_REAL_HOME')

# Setting home as per the confinement
home = snap_real_home if 'SNAP' in os.environ else snap_home

# Load GSettings database
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")

# Get user download dir
download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)

# Check, if the app is running in the sandbox (Flatpak or Snap)
if flatpak:
    try:
      locale = open(f"/app/translations/{r_lang}.json")
    except:
      locale = open(f"/app/translations/en.json")
    version = f"{v}"
    # Directories
    system_dir = "/app"
    CACHE = f"{GLib.get_user_cache_dir()}/tmp"
    DATA = f"{GLib.get_user_data_dir()}"
    # Commands
    periodic_saving_cmd = 'flatpak run io.github.vikdevelop.SaveDesktop --background'
    sync_cmd = "flatpak run io.github.vikdevelop.SaveDesktop --sync"
elif snap:
    try:
      locale = open(f"{os.getenv('SNAP')}/usr/translations/{r_lang}.json")
    except:
      locale = open(f"{os.getenv('SNAP')}/usr/translations/en.json")
    version = f"{v}"
    # Directories
    import dbus
    system_dir = f"{os.getenv('SNAP')}/usr"
    CACHE = f"{os.getenv('SNAP_USER_COMMON')}/.cache/tmp"
    DATA = f"{os.getenv('SNAP_USER_DATA')}/.local/share"
    os.makedirs(f"{CACHE}", exist_ok=True)
    # Commands
    periodic_saving_cmd = 'savedesktop --background'
    sync_cmd = "savedesktop --sync"
else:
    try:
      locale = open(f"{home}/.local/share/savedesktop/translations/{r_lang}.json")
    except:
      locale = open(f"{home}/.local/share/savedesktop/translations/en.json")
    version = f"{v}-native"
    # Directories
    system_dir = f"{home}/.local/share/savedesktop/src"
    CACHE = f"{GLib.get_user_cache_dir()}/io.github.vikdevelop.SaveDesktop"
    DATA = f"{GLib.get_user_data_dir()}/io.github.vikdevelop.SaveDesktop"
    [os.makedirs(path, exist_ok=True) for path in (CACHE, DATA)]
    # Commands
    periodic_saving_cmd = f'savedesktop --background'
    sync_cmd = f"savedesktop --sync"

# Load the translation file
_ = json.load(locale)
