#!/usr/bin/python3
import json, locale, os, socket, subprocess, gi
from pathlib import Path
from gi.repository import Gio, GLib

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
v = "3.5-beta-2024.10.20"
icon = "io.github.vikdevelop.SaveDesktop"
rel_notes = "<p>Fixed minor bugs with showing the button for copying the command for setting up Rclone and temporarily disabled the synchronization option in the Snap environment due to unreliable file system type detection.</p>\
<p>--- 3.5-beta-2024.10.15 ---</p>\
<p>Improved the Initial synchronization setup dialog and other minor UI changes. Also fixed a bug with showing the page about saved or imported configuration</p>\
<p>--- 3.5-beta-2024.10.10 ---</p><ul>\
<li>Simplified the initial setting up synchronization: in that case, it shows the dialog window, which helps you to set it up</li>\
<li>Added more keyboard shortcuts</li>\
<li>Fixed bugs with installation Flatpak apps in the synchronization mode and also with setting the bidirectional sync</li>\
<li>The UI is now more responsive</li>\
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
