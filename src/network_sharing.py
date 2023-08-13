#!/usr/bin/python3
import os
import gi
from gi.repository import Gio

class NetworkSharing:
    def __init__(self):
        self.settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
        
        os.system("python -m http.server")
        
NetworkSharing()
