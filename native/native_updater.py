import requests
import sys
import os
import subprocess
from pathlib import Path

# Get info about version
response = requests.get("https://api.github.com/repos/vikdevelop/SaveDesktop/releases/latest")
github_version = response.json()["tag_name"]

sys.path.append(f"{Path.home()}/.local/share/savedesktop")
os.chdir(f"{Path.home()}/.local/share/savedesktop")
from src.localization import *
os.chdir(f"{Path.home()}/.local/bin")

d_ver = subprocess.getoutput("cat ~/.local/share/io.github.vikdevelop.SaveDesktop/version.txt")

if not d_ver == f"{github_version}":
    os.system("wget -qO /tmp/savedesktop-native-installer.py https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/native_installer.py && python3 /tmp/savedesktop-native-installer.py --remove")
    os.system("wget -qO /tmp/savedesktop-native-installer.py https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/native_installer.py && python3 /tmp/savedesktop-native-installer.py --install")
    os.system(f'echo "{github_version}" > ~/.local/share/io.github.vikdevelop.SaveDesktop/version.txt')
