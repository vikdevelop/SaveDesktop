import os
import sys
import glob
from pathlib import Path
from gi.repository import Gio
from localization import _, DATA
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")

if settings["file-for-syncing"] == "":
    print("Synchronization is not set up.")
    exit()
elif settings["periodic-import"] == "Never2":
    print("Synchronization is not set up.")
else:
    if not os.path.exists(f"{DATA}/synchronization"):
        os.mkdir(f"{DATA}/synchronization")
    if not glob.glob(f"{DATA}/*.sd.tar.gz"):
        os.system(f"cp {settings['file-for-syncing']} {DATA}/synchronization/")
    if not os.path.exists(f"{DATA}/synchronization/file-settings.json"):
        file_name = os.path.basename(settings["file-for-syncing"])
        with open(f"{DATA}/synchronization/file-settings.json", "w") as f:
            f.write('{\n "file-name": "%s.gz",\n "periodic-import": "%s"\n}' % (file_name, settings["periodic-import"]))
    
    path = Path(f'{DATA}/synchronization')

    sys.path.append(path)
    os.chdir(path)
    os.system("python3 -m http.server")
