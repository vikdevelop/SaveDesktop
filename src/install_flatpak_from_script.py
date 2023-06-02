#!/usr/bin/python3
import os
from pathlib import Path

DATA_FLATPAK = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"
DATA_NATIVE = f"{Path.home()}/.local/share/io.github.vikdevelop.SaveDesktop"

if os.path.exists(f"{DATA_FLATPAK}/installed_flatpaks.sh"):
    os.system(f"sh {DATA_FLATPAK}/installed_flatpaks.sh")
    os.system(f"rm {DATA_FLATPAK}/installed_flatpaks.sh")
elif os.path.exists(f"{DATA_NATIVE}/installed_flatpaks.sh"):
    os.system(f"sh {DATA_NATIVE}/installed_flatpaks.sh")
    os.system(f"rm {DATA_NATIVE}/installed_flatpaks.sh")
else:
    print("List with installed Flatpak apps is not exists.")
