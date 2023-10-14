#!/usr/bin/python3
import json
import locale
import os
import socket
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

# Get IP adress of user computer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IPAddr = s.getsockname()[0]
s.close()

# Set application version and icon
v = "2.9.6"
icon = "io.github.vikdevelop.SaveDesktop"

flatpak = os.path.exists("/.flatpak-info")
if flatpak:
    try:
      locale = open(f"/app/translations/{r_lang}.json")
    except:
      locale = open(f"/app/translations/en.json")
    # System, cache and data directories
    system_dir = "/app"
    CACHE = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"
    DATA = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"
    version = f"{v}"
    # Commands
    periodic_saving_cmd = 'flatpak run io.github.vikdevelop.SaveDesktop --background'
    sync_cmd = "flatpak run io.github.vikdevelop.SaveDesktop --sync"
    server_cmd = "flatpak run io.github.vikdevelop.SaveDesktop --start-server"
else:
    try:
      locale = open(f"translations/{r_lang}.json")
    except:
      locale = open(f"translations/en.json")
    # System, cache and data directories
    system_dir = f"{Path.home()}/.local/share/savedesktop/src"
    os.system("mkdir ~/.cache/io.github.vikdevelop.SaveDesktop")
    os.system("mkdir ~/.local/share/io.github.vikdevelop.SaveDesktop")
    CACHE = f"{Path.home()}/.cache/io.github.vikdevelop.SaveDesktop"
    DATA = f"{Path.home()}/.local/share/io.github.vikdevelop.SaveDesktop"
    version = f"{v}-native"
    # Commands
    periodic_saving_cmd = f'savedesktop --background'
    sync_cmd = f"savedesktop --sync"
    server_cmd = f"savedesktop --start-server"

_ = json.load(locale)
