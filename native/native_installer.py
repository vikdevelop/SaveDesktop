#!/usr/bin/python3
import requests
import json
import os
import argparse

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

    # Install files to needed folders
    os.system(f"sh SaveDesktop-{github_version}/native/install_native.sh --install")
    os.system("rm -rf /tmp/SaveDesktop")

if args.remove:
    os.makedirs("/tmp/SaveDesktop", exist_ok=True)
    os.chdir("/tmp/SaveDesktop")
    
    os.system("wget -c https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/install_native.sh")
    os.system("sh install_native.sh --remove")
    
