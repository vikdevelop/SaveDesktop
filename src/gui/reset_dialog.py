import gi, sys, os, subprocess, shutil
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from pathlib import Path
from savedesktop.globals import *

class ResetDialog(Adw.AlertDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.set_heading(_("Reset app settings"))
        self.set_body(_("You will lose all of the app's preferences and settings (e.g. periodic saving or synchronization settings). Your existing archives, whether stored in the cloud or locally, will remain unaffected."))

        self.add_response('cancel', _("Cancel"))
        self.add_response('reset', _("Reset to default"))
        self.set_response_appearance('reset', Adw.ResponseAppearance.DESTRUCTIVE)
        self.connect('response', self.reset_dialog_closed)

    def reset_dialog_closed(self, w, response):
        if response == "reset":
            subprocess.run(["gsettings", "reset-recursively", "io.github.vikdevelop.SaveDesktop"])
            shutil.rmtree(DATA)
            os.execv(sys.executable, [sys.executable] + sys.argv)
