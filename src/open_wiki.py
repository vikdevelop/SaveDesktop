#!/usr/bin/python3
import locale
import json
import os
from localization import *
import subprocess
    
new_lang = p_lang.replace("_", "-")

if "The requested URL returned error: 404" in subprocess.getoutput(f"curl --head --fail https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/translations/wiki/{r_lang}.xml"):
    pb_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/periodic-saving/en"
    flatpak_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/flatpak-apps-installation/en"
    sync_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/synchronization/en"
    enc_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/archive-encryption/en"
    lang_list = True
elif r_lang == "en":
    pb_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/periodic-saving/en"
    flatpak_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/flatpak-apps-installation/en"
    sync_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/synchronization/en"
    enc_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki/archive-encryption/en"
    lang_list = False
else:
    pb_wiki = f"https://vikdevelop.github.io/SaveDesktop/wiki/periodic-saving/{r_lang}"
    flatpak_wiki = f"https://vikdevelop.github.io/SaveDesktop/wiki/flatpak-apps-installation/{r_lang}"
    sync_wiki = f"https://vikdevelop.github.io/SaveDesktop/wiki/synchronization/{r_lang}"
    enc_wiki = f"https://vikdevelop.github.io/SaveDesktop/wiki/archive-encryption/{r_lang}"
    lang_list = False
