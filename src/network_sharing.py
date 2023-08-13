#!/usr/bin/python3
from pathlib import Path
import os
import gi
from gi.repository import Gio

settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")

if settings["file-for-syncing"] == "":
    print("Synchronization is not set up.")
    exit()
if settings["url-for-syncing"] == "":
    print("Synchronization is not set up.")
    exit()

path = Path(settings["file-for-syncing"])
folder = path.parent.absolute()

file_name = os.path.basename(settings["file-for-syncing"])
file = os.path.splitext(file_name)[0]

os.chdir(folder)
os.system(f"wget -c {settings['url-for-syncing']}/{file}.gz")
print("Synchronization has been completed.")
