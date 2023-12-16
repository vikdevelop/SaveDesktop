#!/usr/bin/python3
import locale
import json
import os
from localization import *
import subprocess
    
new_lang = p_lang.replace("_", "-")

if "The requested URL returned error: 404" in subprocess.getoutput(f"curl --head --fail https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/translations/wiki/{r_lang}.xml"):
    pb_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving"
    flatpak_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Save-installed-Flatpak-apps-and-install-it-from-list"
    sync_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network"
    lang_list = False
elif r_lang == "en":
    pb_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving"
    flatpak_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Save-installed-Flatpak-apps-and-install-it-from-list"
    sync_wiki = "https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network"
    lang_list = False
else:
    pb_wiki = f"https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving-{r_lang}" 
    flatpak_wiki = f"https://github.com/vikdevelop/SaveDesktop/wiki/Save-installed-Flatpak-apps-and-install-it-from-list-{r_lang}"
    sync_wiki = f"https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network-{r_lang}"
    lang_list = True
