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
v = "3.5.3"
icon = "io.github.vikdevelop.SaveDesktop"
rel_notes = "<p>Improved an interval logic for periodic saving and synchronization (#373), added Estonian translations thanks to Priit Jõerüüt (Weblate) and fixed minor bugs.</p>\
<p>3.5.2</p>\
<p>Fixed a bug with loading the password requirement in the Cinnamon DE for unlocking the Nextcloud folder, and added a notification about starting synchronization.</p>\
<p>3.5.1</p>\
<ul><li>Fixed the UnboundLocalError when the user selects the Nextcloud drive as a periodic saving folder or cloud drive folder</li>\
<li>Added support for saving the ~/.local/share/gvfs-metadata folder if the Desktop option is enabled</li>\
<li>Added Swedish translations, thanks to @bittin</li></ul>\
<p>3.5</p><ul>\
<li>Added dialog for the initial setting up synchronization; if you have set up synchronization before, it doesn't show</li>\
<li>Temporarily disabled support for synchronization in the Snap environment due to unreliability</li>\
<li>Added more keyboard shortcuts</li>\
<li>Added support for the Hyprland window manager, thanks to @pyclicker</li>\
<li>Fixed bugs with installation Flatpak apps in the synchronization mode and also with setting the bidirectional sync</li>\
<li>The UI is now more adaptive on the smaller screens</li>\
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
