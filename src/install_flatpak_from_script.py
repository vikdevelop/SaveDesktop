#!/usr/bin/python3
import os
from pathlib import Path

flatpak = os.path.exists("/.flatpak-info")

if flatpak:
    DATA = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"
else:
    DATA = f"{Path.home()}/.local/share/io.github.vikdevelop.SaveDesktop"

if os.path.exists(f"{DATA}/installed_flatpaks.sh"):
    os.system(f"sh {DATA}/installed_flatpaks.sh")
    os.system(f"rm {DATA}/installed_flatpaks.sh")
else:
    print("List with installed Flatpak apps is not exists.")
