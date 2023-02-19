#!/usr/bin/python3
import os
import subprocess
import gi
import sys
import json
from datetime import date
from pathlib import Path
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

download_dir = subprocess.getoutput(["xdg-user-dir DOWNLOADS"])
CACHE = f"{Path.home()}/.var/app/com.github.vikdevelop.gnome-config-saver/cache/tmp"
CONFIG = f"{Path.home()}/.var/app/com.github.vikdevelop.gnome-config-saver/config"

class MainWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("GNOME Config Saver")
        self.headerbar = Gtk.HeaderBar.new()
        self.connect("close-request", self.on_close)
        self.set_titlebar(titlebar=self.headerbar)
        self.application = kwargs.get('application')
        
        self.get_settings()
        
        # App menu
        self.menu_button_model = Gio.Menu()
        self.menu_button_model.append("About app", 'app.about')
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.menu_button_model)
        self.headerbar.pack_end(child=self.menu_button)
        
        self.pBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.pBox.set_halign(Gtk.Align.CENTER)
        self.pBox.set_valign(Gtk.Align.CENTER)
        self.pBox.set_margin_start(100)
        self.pBox.set_margin_end(100)
        
        self.toast_overlay = Adw.ToastOverlay.new()
        self.toast_overlay.set_margin_top(margin=1)
        self.toast_overlay.set_margin_end(margin=1)
        self.toast_overlay.set_margin_bottom(margin=1)
        self.toast_overlay.set_margin_start(margin=1)
        
        self.set_child(self.toast_overlay)
        self.toast_overlay.set_child(self.pBox)
        
        self.toast = Adw.Toast.new(title='')
        self.toast.set_timeout(5)
        self.toast.connect('dismissed', self.on_toast_dismissed)
        
        self.label_title = Gtk.Label.new()
        self.label_title.set_markup("<big><b>Welcome to GNOME Config Saver!</b></big> \nThis program allows you to save and load your GNOME configuration. \n \n")
        self.label_title.set_wrap(True)
        self.label_title.set_justify(Gtk.Justification.CENTER)
        self.pBox.append(self.label_title)
        
        self.lbox = Gtk.ListBox.new()
        self.lbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.lbox.get_style_context().add_class(class_name='boxed-list')
        self.pBox.append(self.lbox)
        
        self.sbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.sbox.set_margin_top(9)
        self.sbox.set_margin_bottom(9)
        
        self.ebox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        self.saveEntry = Adw.EntryRow.new()
        self.saveEntry.set_title("Set the file name")
        if os.path.exists(f'{CONFIG}/settings.json'):
            with open(f'{CONFIG}/settings.json') as e:
                jE = json.load(e)
            self.saveEntry.set_text(jE["file-text"])
        self.ebox.append(self.saveEntry)
        
        self.saveButton = Gtk.Button.new_from_icon_name("document-save-symbolic")
        self.saveButton.add_css_class("suggested-action")
        self.saveButton.add_css_class("circular")
        self.saveButton.connect("clicked", self.save_config)
        self.sbox.append(self.saveButton)
        
        self.adw_action_row_save = Adw.ActionRow.new()
        self.adw_action_row_save.set_title("Save GNOME Desktop Configuration")
        self.adw_action_row_save.set_title_lines(3)
        self.adw_action_row_save.set_subtitle("Set the file name without diacritics and spaces")
        self.adw_action_row_save.add_suffix(widget=self.ebox)
        self.adw_action_row_save.add_suffix(widget=self.sbox)
        self.adw_action_row_save.set_activatable_widget(widget=self.saveButton)
        self.lbox.append(child=self.adw_action_row_save)
        
        self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.obox.set_margin_top(7)
        self.obox.set_margin_bottom(7)
        
        self.loadButton = Gtk.Button.new_from_icon_name("image-loading-symbolic")
        self.loadButton.add_css_class("circular")
        self.loadButton.connect("clicked", self.apply_config)
        self.obox.append(self.loadButton)
        
        self.adw_action_row_load = Adw.ActionRow.new()
        self.adw_action_row_load.set_title("Apply GNOME Desktop Configuration")
        self.adw_action_row_load.add_suffix(widget=self.obox)
        self.adw_action_row_load.set_activatable_widget(widget=self.loadButton)
        self.lbox.append(child=self.adw_action_row_load)
        
        self.pBox.append(self.toast_overlay)
        
    def save_config(self, w):
        if not os.path.exists("{}/GNOME_configs/archives".format(download_dir)):
            os.system("mkdir {}/GNOME_configs/archives/".format(download_dir))
        os.system("mkdir -p {}/GNOME_configs/.{} && cp ~/.config/dconf/user {}/GNOME_configs/.{}/".format(download_dir, date.today(), download_dir, date.today()))
        if self.saveEntry.get_text() == "":
            os.system("cd {}/GNOME_configs/.{} && tar --gzip -cf GNOME_config_{}.tar.gz ./".format(download_dir, date.today(), date.today()))
            os.system("mv {}/GNOME_configs/.{}/GNOME_config_{}.tar.gz {}/GNOME_configs/archives/".format(download_dir, date.today(), date.today(), download_dir))
        else:
            os.system("cd {}/GNOME_configs/.{} && tar --gzip -cf {}.tar.gz ./".format(download_dir, date.today(), self.saveEntry.get_text()))
            os.system("mv {}/GNOME_configs/.{}/{}.tar.gz {}/GNOME_configs/archives/".format(download_dir, date.today(), self.saveEntry.get_text(), download_dir))
        self.toast.set_title(title="Configuration has been saved!")
        self.toast.set_button_label("Open the folder")
        self.toast.set_action_name("app.open_dir")
        self.toast_overlay.add_toast(self.toast)
        
    def fileshooser(self):
        self.file_chooser = Gtk.FileChooserDialog()
        self.file_chooser.set_transient_for(self)
        self.file_chooser.set_title('Import GNOME Configuration')
        self.file_chooser.set_action(Gtk.FileChooserAction.OPEN)
        self.file_chooser.add_buttons('Open', Gtk.ResponseType.ACCEPT, \
            'Cancel', Gtk.ResponseType.CANCEL)
        self.file_chooser.set_current_folder( \
            Gio.File.new_for_path(os.environ['HOME']))
        self.file_chooser.set_modal(True)
        self.file_filter = Gtk.FileFilter.new()
        self.file_filter.set_name('Gzip archive')
        self.file_filter.add_pattern('*.tar.gz')
        self.file_chooser.add_filter(self.file_filter)
        self.file_chooser.connect('response', self.open_response)
        self.file_chooser.show()
        
    def open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            dialog.close()
            file = dialog.get_file()
            filename = file.get_path()
            if not os.path.exists("{}/.config".format(Path.home())):
                os.system("mkdir ~/.config/")
            if not os.path.exists("{}/.config/dconf".format(Path.home())):
                os.system("mkdir ~/.config/dconf/")
            os.system("cd %s && tar -xf %s ./" % (CACHE, filename))
            os.system("rm ~/.config/dconf/* && cp %s/user ~/.config/dconf/ && rm %s/*" % (CACHE, CACHE))
            self.toast.set_title(title='The configuration has been applied! Log out and log \nback in for the changes to take effect.')
            self.toast.set_button_label("Log Out")
            self.toast.set_action_name("app.logout")
            self.toast_overlay.add_toast(self.toast)
        else:
            dialog.close()
            
    def apply_config(self, w):
        self.fileshooser()
    
    def on_toast_dismissed(self, toast):
        print('')
        
    def get_settings(self):
        if os.path.exists(f'{CONFIG}/settings.json'):
            with open(f'{CONFIG}/settings.json') as l:
                jL = json.load(l)
            w_width = jL["window_width"]
            w_height = jL["window_height"]
            self.set_default_size(int(w_width), int(w_height))
            self.set_size_request(750, 540)
        else:
            self.set_default_size(750, 540)
            self.set_size_request(750, 540)
    
    def on_close(self, widget, *args):
        with open(f'{CONFIG}/settings.json', 'w') as s:
            s.write('{\n "file-text": "%s",\n "window_width": "%s",\n "window_height": "%s"\n}' % (self.saveEntry.get_text(), self.get_allocation().width, self.get_allocation().height))
        
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('about', self.on_about_action, ["F1"])
        self.create_action('open_dir', self.open_dir)
        self.create_action('logout', self.logout)
        self.connect('activate', self.on_activate)
        
    def open_dir(self, action, param):
        os.system("xdg-open {}/GNOME_configs/archives".format(download_dir))
        
    def logout(self, action, param):
        os.system("dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1")
        
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("GNOME Config Saver")
        dialog.set_version("1.0")
        dialog.set_developer_name("vikdevelop")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/gnome-config-saver")
        dialog.set_issue_url("https://github.com/vikdevelop/gnome-config-saver/issues")
        dialog.set_copyright("© 2023 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("com.github.vikdevelop.gnome-config-saver")
        dialog.show()    
    
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
    
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()
app = MyApp()
app.run(sys.argv)
