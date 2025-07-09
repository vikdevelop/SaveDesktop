import sys, gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio
from localization import *
from password_store import *

class PasswordWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(f"{_['sync']} | Save Desktop")
        
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
        self.titleRow.set_title(_["enter_password_title"])
        self.titleRow.set_title_lines(3)
        self.titleRow.set_subtitle(_["enter_password_desc"])
        self.titleRow.set_size_request(10, -1)
        self.titleRow.set_subtitle_lines(10)
        self.winBox.append(self.titleRow)
        
        # Password Entry
        self.passEntry = Adw.PasswordEntryRow.new()
        self.passEntry.set_title(_["password_entry"])
        self.winBox.append(self.passEntry)
        
        # Switch and row for showing the "Remember a password" option
        self.remSwitch = Gtk.Switch.new()
        self.remSwitch.set_valign(Gtk.Align.CENTER)
        self.remSwitch.set_active(True)
        
        self.remRow = Adw.ActionRow.new()
        self.remRow.set_title(_["remember_password"])
        self.remRow.add_suffix(self.remSwitch)
        self.remRow.set_activatable_widget(self.remSwitch)
        self.winBox.append(self.remRow)
        
        self.applyButton = Gtk.Button.new_with_label(_["apply"])
        self.applyButton.add_css_class('suggested-action')
        self.applyButton.add_css_class('pill')
        self.applyButton.set_halign(Gtk.Align.CENTER)
        self.applyButton.connect("clicked", self.save_password)
        self.winBox.append(self.applyButton)
        
    # Save the entered password to the file
    def save_password(self, w):
        if self.remSwitch.get_active():
            PasswordStore(self.passEntry.get_text())
        else:
            with open(f"{DATA}/entered-password.txt", "w") as ep:
                ep.write(self.passEntry.get_text())
        app.quit()
        
class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE,
                         application_id="io.github.vikdevelop.SaveDesktop" if not snap else None)
        self.connect('activate', self.on_activate)
    
    # Show the main window of the application
    def on_activate(self, app):
        self.win = PasswordWindow(application=app)
        self.win.present()

app = App()
app.run(sys.argv)
