import os
import sys
from pathlib import Path
from gi.repository import Gio
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
path = Path(settings["file-for-syncing"])
folder = path.parent.absolute()

sys.path.append(folder)
os.chdir(folder)
os.system("python -m http.server")
