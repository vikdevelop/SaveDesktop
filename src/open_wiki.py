#!/usr/bin/python3
import locale
import json
import os
import subprocess
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
    
new_lang = p_lang.replace("_", "-")

if "The requested URL returned error: 404" in subprocess.getoutput(f"curl --head --fail https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/translations/wiki/{r_lang}.xml"):
    pb_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving"
    flatpak_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Save-installed-Flatpak-apps-and-install-it-from-list"
    sync_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network"
elif r_lang == "en":
    pb_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving"
    flatpak_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Save-installed-Flatpak-apps-and-install-it-from-list"
    sync_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network"
else:
    pb_wiki = f"https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving-{new_lang}" 
    flatpak_wiki = f"https://github.com/vikdevelop/SaveDesktop/wiki/Save-installed-Flatpak-apps-and-install-it-from-list-{new_lang}"
    sync_wiki = f"https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network-{new_lang}"
