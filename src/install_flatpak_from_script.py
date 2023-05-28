#!/usr/bin/python3
import os
from pathlib import Path

flatpak = os.path.exists("/.flatpak-info")

DATA = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"

if os.path.exists(f"{DATA}/installed_flatpaks.sh"):
    os.system(f"sh {DATA}/installed_flatpaks.sh")
    os.system(f"rm {DATA}/installed_flatpaks.sh")
else:
    print("List with installed Flatpak apps is not exists.")
