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
CACHE = f"{Path.home()}/.var/app/com.github.vikdevelop.SaveDesktop/cache/tmp"
CONFIG = f"{Path.home()}/.var/app/com.github.vikdevelop.SaveDesktop/config"

class MainWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("SaveDesktop")
        self.headerbar = Gtk.HeaderBar.new()
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
        
        if os.getenv('XDG_CURRENT_DESKTOP') == 'GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
            self.environment = 'COSMIC'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'X-Cinnamon':
            self.environment = 'Cinnamon'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Budgie:GNOME':
            self.environment = 'Budgie'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
            self.environment = 'Xfce'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        else:
            self.Image = Gtk.Image.new_from_icon_name("exclamation_mark")
            self.Image.set_pixel_size(50)
            self.pBox.append(self.Image)
            self.label_sorry = Gtk.Label()
            self.label_sorry.set_markup("<big><b>You have an unsupported environment installed.</b></big> \nPlease use this environments: GNOME, COSMIC, Cinnamon, Budgie or Xfce.")
            self.label_sorry.set_wrap(True)
            self.label_sorry.set_justify(Gtk.Justification.CENTER)
            self.pBox.append(self.label_sorry)
        
    def save_desktop(self):
        self.label_title = Gtk.Label.new()
        self.label_title.set_markup("<big><b>Welcome to SaveDesktop for {}</b></big> \nThis program allows you to save and load your {} configuration. \n \n".format(self.environment, self.environment))
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
        self.saveButton.connect("clicked", self.set_title_t)
        self.sbox.append(self.saveButton)
        
        self.adw_action_row_save = Adw.ActionRow.new()
        self.adw_action_row_save.set_title("Save {} Desktop Configuration".format(self.environment))
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
        self.adw_action_row_load.set_title("Apply {} Desktop Configuration".format(self.environment))
        self.adw_action_row_load.add_suffix(widget=self.obox)
        self.adw_action_row_load.set_activatable_widget(widget=self.loadButton)
        self.lbox.append(child=self.adw_action_row_load)
        
        self.pBox.append(self.toast_overlay)
        
    def set_title_t(self, w):
        self.toast.set_title("Please wait...")
        self.save_config()
    
    def save_config(self):
        if not os.path.exists("{}/SaveDesktop/".format(download_dir)):
            os.system("mkdir {}/SaveDesktop/".format(download_dir))
        if not os.path.exists("{}/SaveDesktop/archives".format(download_dir)):
            os.system("mkdir {}/SaveDesktop/archives/".format(download_dir))
        os.system("mkdir -p {}/SaveDesktop/.{} && cd {}/SaveDesktop/.{}".format(download_dir, date.today(), download_dir, date.today()))
        os.chdir('{}/SaveDesktop/.{}'.format(download_dir, date.today()))
        os.system('cp ~/.config/dconf/user ./')
        os.system('cp -R ~/.local/share/backgrounds ./')
        os.system('cp -R ~/.local/share/icons ./')
        os.system('cp -R ~/.themes ./')
        # Save configs on individual desktop environments
        if self.environment == 'GNOME':
            os.popen("cp -R ~/.local/share/gnome-background-properties ./")
            os.popen("cp -R ~/.local/share/gnome-shell ./")
            os.popen("cp -R ~/.local/share/nautilus-python ./")
            os.popen("cp -R ~/.config/gnome-control-center ./")
        elif self.environment == 'Cinnamon':
            os.popen("cp -R ~/.config/nemo ./")
            os.popen("cp -R ~/.local/share/cinnamon ./")
            os.popen("cp -R ~/.cinnamon ./")
        elif self.environment == 'Budgie':
            os.popen("cp -R ~/.config/budgie-desktop ./")
            os.popen("cp -R ~/.config/budgie-extras ./")
            os.popen("cp -R ~/.config/nemo ./")
        elif self.environment == 'COSMIC':
            os.popen("cp -R ~/.config/pop-shell ./")
            os.popen("cp -R ~/.local/share/gnome-shell ./")
        elif self.environment == 'Xfce':
            os.popen("cp -R ~/.config/xfce4 ./")
            os.popen("cp -R ~/.config/Thunar ./")
            
        # Get self.saveEntry text
        if self.saveEntry.get_text() == "":
            os.popen("tar --gzip -cf {}_config_{}.tar.gz ./".format(self.environment, date.today()))
            os.popen("mv {}/SaveDesktop/.{}/{}_config_{}.tar.gz {}/SaveDesktop/archives/".format(download_dir, date.today(), self.environment, date.today(), download_dir))
        else:
            os.popen("tar --gzip -cf {}.tar.gz ./".format(self.saveEntry.get_text()))
            os.popen("mv {}/SaveDesktop/.{}/{}.tar.gz {}/SaveDesktop/archives/".format(download_dir, date.today(), self.saveEntry.get_text(), download_dir))
        self.exporting_done()
            
    def exporting_done(self):
        self.toast.set_title(title="Configuration has been saved!")
        self.toast.set_button_label("Open the folder")
        self.toast.set_action_name("app.open_dir")
        self.toast_overlay.add_toast(self.toast)
        
    def fileshooser(self):
        self.file_chooser = Gtk.FileChooserDialog()
        self.file_chooser.set_transient_for(self)
        self.file_chooser.set_title('Import {} Configuration'.format(self.environment))
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
            # Applying configuration for GNOME-based environments
            if not os.path.exists("{}/.config".format(Path.home())):
                os.system("mkdir ~/.config/")
            if not os.path.exists("{}/.config/dconf".format(Path.home())):
                os.system("mkdir ~/.config/dconf/")
            os.chdir("%s" % CACHE)
            os.system("tar -xf %s ./" % filename)
            os.system("rm ~/.config/dconf/* && cp ./user ~/.config/dconf/")
            os.popen('cp -R ./icons ~/.local/share/')
            os.popen('cp -R ./.themes ~/')
            os.popen("cp -R ./backgrounds ~/.local/share/")
            # Apply configs for individual desktop environments
            if self.environment == 'GNOME':
                os.popen("cp -R ./gnome-background-properties ~/.local/share/")
                os.popen("cp -R ./gnome-shell ~/.local/share/")
                os.popen("cp -R ./nautilus-python ~/.local/share/")
                os.popen("cp -R ./gnome-control-center ~/.config/")
            elif self.environment == 'Cinnamon':
                os.popen("cp -R ./nemo ~/.config/")
                os.popen("cp -R ./cinnamon ~/.local/share/")
                os.popen("cp -R ./.cinnamon ~/")
            elif self.environment == 'Budgie':
                os.popen("cp -R ./budgie-desktop ~/.config/")
                os.popen("cp -R ./budgie-extras ~/.config/")
                os.popen("cp -R ./nemo ~/.config/")
            elif self.environment == 'COSMIC':
                os.popen("cp -R ./pop-shell ~/.config/")
                os.popen("cp -R ./gnome-shell ~/.local/share/")
            elif self.environment == 'Xfce':
                os.popen("cp -R ./xfce4 ~/.config/")
                os.popen("cp -R ./Thunar ~/.config/")
            self.applying_done()
        else:
            dialog.close()
            
    def apply_config(self, w):
        self.fileshooser()
    
    def applying_done(self):
        self.toast.set_title(title='The configuration has been applied! Log out and log \nback in for the changes to take effect.')
        self.toast.set_button_label("Log Out")
        self.toast.set_action_name("app.logout")
        self.toast_overlay.add_toast(self.toast)
    
    def on_toast_dismissed(self, toast):
        print('')
        os.system("rm %s/*" % CACHE)
        
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
        os.system("xdg-open {}/SaveDesktop/archives".format(download_dir))
        
    def logout(self, action, param):
        os.system("rm %s/*" % CACHE)
        if os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
            os.system("dbus-send --session --type=method_call --print-reply --dest=org.xfce.SessionManager /org/xfce/SessionManager org.xfce.Session.Manager.Logout boolean:true boolean:false")
        else:
            os.system("dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1")
        
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("SaveDesktop")
        dialog.set_version("1.0")
        dialog.set_developer_name("vikdevelop")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/SaveDesktop")
        dialog.set_issue_url("https://github.com/vikdevelop/SaveDesktop")
        dialog.set_copyright("© 2023 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("com.github.vikdevelop.SaveDesktop")
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
