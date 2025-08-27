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

# Set application version, icon, and release notes
v = "3.6.2"
icon = "io.github.vikdevelop.SaveDesktop"
rel_notes = "<ul>\
<li>Fixed a bug with properly including extensions in the archive (#428)</li>\
<li>Fixed a bug with importing a configuration from the folder</li>\
<li>Fixed a bug with cancelling saving or importing configuration</li>\
<li>Fixed a bug with crashing the app after setting up the synchronization</li>\
<li>Added the Ctrl+W keyboard shortcut for closing the app window</li></ul>\
<p>3.6.1</p><p>This version brings significant speedup of saving and importing configurations thanks to parallel copying (thanks to @ArthurValadares), change of application name from \"SaveDesktop\" to \"Save Desktop\" and minor user interface improvements along with minor bug fixes. Also improved the import of dynamic wallpapers in GNOME and improved archive encryption.</p>\
<p>3.6-hotfix</p><p>Fixed a \"buffer overflow\" error when creating configuration archives by replacing the ZIP utility with 7-Zip.</p>\
<p>3.6</p><ul>\
<li>Added an option to encrypt the periodic saving files and added support for its usage in the synchronization mode</li>\
<li>Migrated from the *.sd.tar.gz to the *.sd.zip archive format, but for backward compatibility reasons, it will still be possible to select the first named archive format</li>\
<li>Added support for using the syncthing folders in the synchronization mode (#392)</li>\
<li>Fixed other minor bugs</li>\
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

# Get the user download dir
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
    version = f"{v}-snap"
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
