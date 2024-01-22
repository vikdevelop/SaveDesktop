#!/usr/bin/python3
import json
import locale
import os
import socket
import subprocess
from pathlib import Path

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

# Get IP address of user computer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IPAddr = s.getsockname()[0]
s.close()

# Set application version, and icon
v = "3.0.1"
icon = "io.github.vikdevelop.SaveDesktop"
rel_notes = "<p>FIxed these bugs:</p>\
<ul>\
<li>If your archive has a directory with Flatpak app data, the cache will not be removed after closing the app; it will be removed after finished copying the data</li>\
<li>If the content in the folder of Flatpak apps data in your configuration archive is the same as the ~/.var/app folder, the data will not be copy</li>\
</ul>\
<p>And also:</p>\
<ul><li>Updated translations</li></ul>"

flatpak = os.path.exists("/.flatpak-info")
snap = os.environ.get('SNAP_NAME', '') == 'savedesktop'

#Checking for Snap and Real Home directories

snap_home = Path.home()#keeping this value if it comes handy
snap_real_home = os.getenv('SNAP_REAL_HOME')

#Setting home as per the confinement
home = snap_real_home if 'SNAP' in os.environ else snap_home

if flatpak:
    try:
      locale = open(f"/app/translations/{r_lang}.json")
    except:
      locale = open(f"/app/translations/en.json")
    # System, cache and data directories
    system_dir = "/app"
    CACHE = f"{home}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"
    DATA = f"{home}/.var/app/io.github.vikdevelop.SaveDesktop/data"
    version = f"{v}"
    # Commands
    periodic_saving_cmd = 'flatpak run io.github.vikdevelop.SaveDesktop --background'
    sync_cmd = "flatpak run io.github.vikdevelop.SaveDesktop --sync"
    server_cmd = "flatpak run io.github.vikdevelop.SaveDesktop --start-server"
elif snap:
    try:
      locale = open(f"{os.getenv('SNAP')}/usr/translations/{r_lang}.json")
    except:
      locale = open(f"{os.getenv('SNAP')}/usr/translations/en.json")
    system_dir = f"{os.getenv('SNAP')}/usr"
    version = f"{v}"
    periodic_saving_cmd = 'savedesktop --background'
    sync_cmd = "savedesktop --sync"
    server_cmd = "savedesktop --start-server"
    CACHE = f"{os.getenv('SNAP_USER_COMMON')}/.cache/tmp"
    DATA = f"{os.getenv('SNAP_USER_DATA')}/.local/share"
else:
    try:
      locale = open(f"{home}/.local/share/savedesktop/translations/{r_lang}.json")
    except:
      locale = open(f"{home}/.local/share/savedesktop/translations/en.json")
    # System, cache and data directories
    system_dir = f"{home}/.local/share/savedesktop/src"
    os.system("mkdir ~/.cache/io.github.vikdevelop.SaveDesktop")
    os.system("mkdir ~/.local/share/io.github.vikdevelop.SaveDesktop")
    CACHE = f"{home}/.cache/io.github.vikdevelop.SaveDesktop"
    DATA = f"{home}/.local/share/io.github.vikdevelop.SaveDesktop"
    version = f"{v}-native"
    # Commands
    periodic_saving_cmd = f'savedesktop --background'
    sync_cmd = f"savedesktop --sync"
    server_cmd = f"savedesktop --start-server"

_ = json.load(locale)
