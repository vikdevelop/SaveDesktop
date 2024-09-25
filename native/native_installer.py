#!/usr/bin/python3
import requests
import json
import os
import argparse
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

# Check GTK and LibAdwaita versions
gtk_ver = f"{Gtk.MAJOR_VERSION}.{Gtk.MINOR_VERSION}"
adw_ver = f"{Adw.MAJOR_VERSION}.{Adw.MINOR_VERSION}"

if gtk_ver < "4.14" or adw_ver < "1.5":
    print(f"You have installed an unsupported version of the GTK and LibAdwaita libraries, specifically you have GTK {gtk_ver} and LibAdwaita {adw_ver}. For proper functionality, you must have at least GTK 4.14 and LibAdwaita 1.5.")
    print("If you want a simple solution to this problem, please install the Flatpak or Snap packages, which have available the necessary libraries available. The instructions are available here: https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#installation")
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
    os.makedirs("/tmp/SaveDesktop", exist_ok=True)
    os.chdir("/tmp/SaveDesktop")
    os.system(f"wget -c https://github.com/vikdevelop/SaveDesktop/archive/refs/tags/{github_version}.tar.gz")
    os.system("tar -xf *.tar.gz")
    os.chdir(f"SaveDesktop-{github_version}")
    
    # Install files to needed folders
    os.system("wget -c https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/install_native.sh") # get the latest Bash script for installing to the specific directories
    os.system(f"sh install_native.sh --install")
    os.system("rm -rf /tmp/SaveDesktop")

if args.remove:
    os.makedirs("/tmp/SaveDesktop", exist_ok=True)
    os.chdir("/tmp/SaveDesktop")
    os.system("wget -c https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/install_native.sh")
    os.system("sh install_native.sh --remove")
    os.system("rm -rf /tmp/SaveDesktop")
