#!/usr/bin/python3
import requests
import json
import os
import argparse
try:
    import gi
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except Exception as e:
    print('\033[1m' + 'You have not installed the necessary libraries:' + '\033[0m')
    print(e)
    print("If you want a simple solution to this problem, please install the Flatpak or Snap packages, which have available the necessary libraries. The instructions are available here: https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#installation")
    exit()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--install", help="Install SaveDesktop", action="store_true")
parser.add_argument("-i", "--remove", help="Remove SaveDesktop", action="store_true")

args = parser.parse_args()

if args.install:
    # Get info about version
    response = requests.get("https://api.github.com/repos/vikdevelop/SaveDesktop/releases/latest")
    github_version = response.json()["tag_name"]

    # Download and decompress archive from Github
    if not os.path.exists("/tmp/SaveDesktop"):
        os.mkdir("/tmp/SaveDesktop")
    os.chdir("/tmp/SaveDesktop")
    os.system(f"wget -c https://github.com/vikdevelop/SaveDesktop/archive/refs/tags/{github_version}.tar.gz")
    os.system("tar -xf *.tar.gz")
    os.chdir(f"SaveDesktop-{github_version}")
    
    # Install files to needed folders
    os.system(f"sh native/install_native.sh --install")
    os.system("rm -rf /tmp/SaveDesktop")

if args.remove:
    os.system("wget -c https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/install_native.sh")
    os.system("sh install_native.sh --remove")
    
