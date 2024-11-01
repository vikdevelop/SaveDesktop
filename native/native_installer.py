#!/usr/bin/python3
import requests, json, os, sys, argparse, gi
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
parser.add_argument("--install", help="Install SaveDesktop", action="store_true")
parser.add_argument("--remove", help="Remove SaveDesktop", action="store_true")
parser.add_argument("--update", help="Update SaveDesktop", action="store_true")

args = parser.parse_args()

def install(github_version):
    os.makedirs("/tmp/SaveDesktop", exist_ok=True)
    os.chdir("/tmp/SaveDesktop")
    os.system(f"wget -c https://github.com/vikdevelop/SaveDesktop/archive/refs/tags/{github_version}.tar.gz")
    os.system("tar -xf *.tar.gz")
    os.chdir(f"SaveDesktop-{github_version}")
    
    os.system("wget -c https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/install_native.sh")
    os.system("sh directories.sh --install")
    os.system("rm -rf /tmp/SaveDesktop")

def remove():
    os.makedirs("/tmp/SaveDesktop", exist_ok=True)
    os.chdir("/tmp/SaveDesktop")
    os.system("wget -c https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/install_native.sh")
    os.system("sh directories.sh --remove")
    os.system("rm -rf /tmp/SaveDesktop")

if args.install:
    response = requests.get("https://api.github.com/repos/vikdevelop/SaveDesktop/releases/latest")
    github_version = response.json()["tag_name"]
    install(github_version)

if args.remove:
    remove()

if args.update:
    response = requests.get("https://api.github.com/repos/vikdevelop/SaveDesktop/releases/latest")
    github_version = response.json()["tag_name"]
    
    sys.path.append(f"{Path.home()}/.local/share/savedesktop")
    os.chdir(f"{Path.home()}/.local/share/savedesktop")
    from src.localization import *
    os.chdir(f"{Path.home()}/.local/bin")
    
    d_ver = subprocess.getoutput("cat ~/.local/share/io.github.vikdevelop.SaveDesktop/version.txt")
    
    if not d_ver == f"{github_version}":
        remove()
        
        install(github_version)
        
        with open(Path.home() / ".local/share/io.github.vikdevelop.SaveDesktop/version.txt", "w") as version_file:
            version_file.write(github_version)
