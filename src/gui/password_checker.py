import sys, gi, gettext, locale
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio
from savedesktop.globals import *
from savedesktop.core.password_store import *

class PasswordWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        sync = _("Sync")
        self.set_title(f"{sync} | Save Desktop")
        
        # Header bar
        self.headerbar = Gtk.HeaderBar.new()
        self.headerbar.pack_start(Gtk.Image.new_from_icon_name("io.github.vikdevelop.SaveDesktop-symbolic"))
        self.set_titlebar(self.headerbar)
        
        self.set_default_size(400, 200)
        self.set_resizable(False)
        
        # The main box
        self.winBox = Gtk.ListBox.new()
        self.winBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.winBox.add_css_class('boxed-list')
        self.winBox.set_size_request(-1, -1)
        self.winBox.set_margin_start(20)
        self.winBox.set_margin_end(20)
        self.winBox.set_margin_top(20)
        self.winBox.set_margin_bottom(20)
        self.set_child(self.winBox)
        
        # Label
        self.titleRow = Adw.ActionRow.new()
        self.titleRow.set_title(_("Please enter a password to unlock the archive for sync the configuration"))
        self.titleRow.set_title_lines(3)
        self.titleRow.set_subtitle(_("An encrypted archive has been selected for synchronization using the Save Desktop app. Please enter the password below to unlock it and start synchronization."))
        self.titleRow.set_size_request(10, -1)
        self.titleRow.set_subtitle_lines(10)
        self.winBox.append(self.titleRow)
        
        # Password Entry
        self.passEntry = Adw.PasswordEntryRow.new()
        self.passEntry.set_title(_("Password"))
        self.passEntry.connect("changed", self._empty_check)
        self.winBox.append(self.passEntry)
        
        # Switch and row for showing the "Remember a password" option
        self.remSwitch = Gtk.Switch.new()
        self.remSwitch.set_valign(Gtk.Align.CENTER)
        self.remSwitch.set_active(True)
        
        self.remRow = Adw.ActionRow.new()
        self.remRow.set_title(_("Remember Password"))
        self.remRow.add_suffix(self.remSwitch)
        self.remRow.set_activatable_widget(self.remSwitch)
        self.winBox.append(self.remRow)
        
        self.applyButton = Gtk.Button.new_with_label(_("Apply"))
        self.applyButton.add_css_class('suggested-action')
        self.applyButton.add_css_class('pill')
        self.applyButton.set_halign(Gtk.Align.CENTER)
        self.applyButton.connect("clicked", self.save_password)
        self.applyButton.set_sensitive(False)
        self.winBox.append(self.applyButton)
        
    # Set sensitivity of the Apply button based on the Password entry status
    def _empty_check(self, passEntry):
        if self.passEntry.get_text() == "":
            self.applyButton.set_sensitive(False)
        else:
            self.applyButton.set_sensitive(True)

    # Save the entered password to the file
    def save_password(self, w):
        if self.remSwitch.get_active():
            PasswordStore(self.passEntry.get_text())
        else:
            with open(f"{CACHE}/temp_file", "w") as ep:
                ep.write(self.passEntry.get_text())
        self.close()
        
class PasswordCheckerApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE,
                         application_id="io.github.vikdevelop.SaveDesktop")
        self.connect('activate', self.on_activate)
    
    # Show the app window
    def on_activate(self, app):
        self.win = PasswordWindow(application=app)
        self.win.present()
