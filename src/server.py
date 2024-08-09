import os
import sys
import glob
from pathlib import Path
from gi.repository import Gio
from localization import _, DATA
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")

if settings["file-for-syncing"] == "":
    print("Synchronization is not set up. The synchronization file is missing.")
    exit()
elif settings["periodic-saving"] == "Never":
    print("Periodic saving is set to the Never. Please change it.")
    exit()
else:
    if not os.path.exists(f"{DATA}/synchronization"):
        os.mkdir(f"{DATA}/synchronization")
    if not glob.glob(f"{DATA}/synchronization/*.sd.tar.gz"):
        os.system(f"cp {settings['file-for-syncing']} {DATA}/synchronization/")
    
    path = Path(f'{DATA}/synchronization')

    sys.path.append(path)
    os.chdir(path)
    os.system("python3 -m http.server")
