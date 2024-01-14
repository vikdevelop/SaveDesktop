import requests
import sys
import os
from pathlib import Path

# Get info about version
response = requests.get("https://api.github.com/repos/vikdevelop/SaveDesktop/releases/latest")
github_version = response.json()["name"]

sys.path.append(f"{Path.home()}/.local/share/savedesktop")
os.chdir(f"{Path.home()}/.local/share/savedesktop")
from src.localization import *
os.chdir(f"{Path.home()}/.local/bin")

d_ver = version.replace("-native", "")

if not d_ver >= f"{github_version}":
    os.system("git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop && sh /tmp/SaveDesktop/install_native.sh --remove")
    os.system("git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop && sh /tmp/SaveDesktop/install_native.sh --install")
