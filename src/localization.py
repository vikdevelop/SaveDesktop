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

# Get IP address of device for synchronizing computers in the network
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    s.close()
except Exception as err:
    IPAddr = f"ERR: {err}"

# Set application version, and icon
v = "3.4-beta-05"
icon = "io.github.vikdevelop.SaveDesktop.Devel"
rel_notes = "<p>3.4-beta-05</p>\
<p>Fixed bugs related to importing encrypted archives in the CLI interface, added more messages in the GUI in the error occur case, and excluded the cache directories of Flatpak apps in the configuration archive.</p>\
<p>3.4-beta-04</p>\
<ul>\
<li>Fixed some bugs with setting up synchronization such as periodic synchronization interval selection or starting the HTTP server in the case if the selected synchronization in the local network only</li>\
<li>Sped up the configuration import, because files that are unchanged will no longer be copied (this also applies to Flatpak app installations)</li>\
<li>If an error occurs during saving or importing configuration, e.g., while copying the archive to the user-defined folder, it shows a message in the graphical user interface</li>\
<li>In the cloud folder detection as the periodic saving folder case, the application will let you know by the icon next to the periodic saving file row in the 'Set up the sync file' dialog</li>\
</ul>\
<p>3.4-beta-03</p>\
<ul>\
<li>Simplified setting up the synchronization with the cloud folder process: on the Sync page, just click on the \"Set up the sync file\" button and make the changes required by the application</li>\
<li>Added possibility to set up smaller window size</li>\
</ul>\
<p>3.4-beta-02</p>\
<ul><li>Changed descriptions in the \"Connect with other computer\" dialog</li></ul>\
<p>3.4-beta</p>\
<ul>\
<li>Added support for cloud synchronization: however, you need to have a folder on your computer that will be synchronized with your cloud storage, for example via GNOME Online Accounts.</li>\
<li>Added an option to generate a password for the configuration archive, about 24 characters long</li>\
</ul>"

flatpak = os.path.exists("/.flatpak-info")
snap = os.environ.get('SNAP_NAME', '') == 'savedesktop'

# Checking for Snap and Real Home directories

snap_home = Path.home()#keeping this value if it comes handy
snap_real_home = os.getenv('SNAP_REAL_HOME')

# Setting home as per the confinement
home = snap_real_home if 'SNAP' in os.environ else snap_home

if flatpak:
    try:
      locale = open(f"/app/translations/{r_lang}.json")
    except:
      locale = open(f"/app/translations/en.json")
    version = f"{v}"
    # Directories
    system_dir = "/app"
    CACHE = f"{home}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"
    DATA = f"{home}/.var/app/io.github.vikdevelop.SaveDesktop/data"
    # Commands
    periodic_saving_cmd = 'flatpak run io.github.vikdevelop.SaveDesktop --background'
    sync_cmd = "flatpak run io.github.vikdevelop.SaveDesktop --sync"
    server_cmd = "flatpak run io.github.vikdevelop.SaveDesktop --start-server"
elif snap:
    try:
      locale = open(f"{os.getenv('SNAP')}/usr/translations/{r_lang}.json")
    except:
      locale = open(f"{os.getenv('SNAP')}/usr/translations/en.json")
    version = f"{v}"
    # Directories
    system_dir = f"{os.getenv('SNAP')}/usr"
    CACHE = f"{os.getenv('SNAP_USER_COMMON')}/.cache/tmp"
    DATA = f"{os.getenv('SNAP_USER_DATA')}/.local/share"
    # Commands
    periodic_saving_cmd = 'savedesktop --background'
    sync_cmd = "savedesktop --sync"
    server_cmd = "savedesktop --start-server"
else:
    try:
      locale = open(f"{home}/.local/share/savedesktop/translations/{r_lang}.json")
    except:
      locale = open(f"{home}/.local/share/savedesktop/translations/en.json")
    version = f"{v}-native"
    # Directories
    system_dir = f"{home}/.local/share/savedesktop/src"
    CACHE = f"{home}/.cache/io.github.vikdevelop.SaveDesktop"
    DATA = f"{home}/.local/share/io.github.vikdevelop.SaveDesktop"
    # Commands
    periodic_saving_cmd = f'savedesktop --background'
    sync_cmd = f"savedesktop --sync"
    server_cmd = f"savedesktop --start-server"

_ = json.load(locale)
