#!/usr/bin/python3
import os
import tarfile
import subprocess
import gi
import sys
import json
from datetime import date
from pathlib import Path
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk, GObject

# Czech
if subprocess.getoutput('locale | grep "LANG"') == 'LANG=cs_CZ.UTF-8':
    lang = 'cs.json'
# French
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=fr_FR.UTF-8':
    lang = 'fr.json'
# Portugalese (Brasil)    
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=pt_BR.UTF-8':
    lang = 'pt_BR.json'
# Italian    
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=it_IT.UTF-8':
    lang = 'it.json'
# Dutch
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=nl_NL.UTF-8':
    lang = 'nl.json'
# Arabic
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=ar_SA.UTF-8':
    lang = 'ar.json'
# Russian
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=ru_RU.UTF-8':
    lang = 'ru.json'
# Indonesian
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=id_ID.UTF-8':
    lang = 'id.json'
# Norwegian (Bokmål)
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=nb_NO.UTF-8':
    lang = 'nb_NO.json'
# Ukrainian
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=uk_UA.UTF-8':
    lang = 'uk.json'
# Hungarian
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=hu_HU.UTF-8':
    lang = 'hu.json'
# Spanish
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=es_ES.UTF-8':
    lang = 'es.json'
# English
else:
    lang = 'en.json'

locale = open(f"/app/translations/{lang}")
_ = json.load(locale)

download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
CACHE = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"
CONFIG = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/config"

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
        self.menu_button_model.append(_["about_app"], 'app.about')
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.menu_button_model)
        self.headerbar.pack_end(child=self.menu_button)
        
        # Drag and drop area
        drag_source = Gtk.DragSource.new()
        drag_source.set_actions(Gdk.DragAction.COPY)
        drag_source.connect('prepare', self.on_prepare)
        drag_source.connect('drag-begin', self.on_drag_begin)
        drag_source.connect('drag-end', self.on_drag_end)
        drag_source.connect('drag-cancel', self.on_drag_cancel)

        drop_target = Gtk.DropTarget.new(GObject.TYPE_STRING, Gdk.DragAction.COPY)
        drop_target.connect('drop', self.on_drop)

        self.add_controller(drag_source)
        self.add_controller(drop_target)
        
        # Primary layout
        self.pBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.pBox.set_halign(Gtk.Align.CENTER)
        self.pBox.set_valign(Gtk.Align.CENTER)
        self.pBox.set_margin_start(100)
        self.pBox.set_margin_end(100)
        
        # Toast
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
        
        # check of user current desktop
        if os.getenv('XDG_CURRENT_DESKTOP') == 'GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'zorin:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'ubuntu:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
            self.environment = 'COSMIC'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Pantheon':
            self.environment = 'Pantheon'
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
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'MATE':
            self.environment = 'MATE'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        else:
            self.Image = Gtk.Image.new_from_icon_name("exclamation_mark")
            self.Image.set_pixel_size(50)
            self.pBox.append(self.Image)
            self.label_sorry = Gtk.Label()
            self.label_sorry.set_markup(_["unsuppurted_env_desc"].format("GNOME, Xfce, Budgie, Cinnamon, COSMIC, Pantheon, MATE"))
            self.label_sorry.set_wrap(True)
            self.label_sorry.set_justify(Gtk.Justification.CENTER)
            self.pBox.append(self.label_sorry)
    
    # Show main layout
    def save_desktop(self):
        self.titleImage = Gtk.Image.new_from_icon_name("io.github.vikdevelop.SaveDesktop")
        self.titleImage.set_pixel_size(64)
        self.pBox.append(self.titleImage) 
        
        self.label_title = Gtk.Label.new()
        self.label_title.set_markup(_["savedesktop_title"].format(self.environment))
        self.pBox.append(self.label_title)
        
        self.label_export = Gtk.Label.new()
        self.label_export.set_markup(f'<b>{_["save_config"]}</b>')
        self.label_export.set_xalign(-1)
        self.pBox.append(self.label_export)
        
        self.lbox_e = Gtk.ListBox.new()
        self.lbox_e.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.lbox_e.get_style_context().add_class(class_name='boxed-list')
        self.pBox.append(self.lbox_e)
        
        self.label_import = Gtk.Label.new()
        self.label_import.set_markup(f'<b>{_["import_config"]}</b>')
        self.label_import.set_xalign(-1)
        self.pBox.append(self.label_import)
        
        self.lbox_a = Gtk.ListBox.new()
        self.lbox_a.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.lbox_a.get_style_context().add_class(class_name='boxed-list')
        self.pBox.append(self.lbox_a)
        
        self.saveEntry = Adw.EntryRow.new()
        self.saveEntry.set_title(_["set_filename"])
        if os.path.exists(f'{CONFIG}/settings.json'):
            with open(f'{CONFIG}/settings.json') as e:
                jE = json.load(e)
            self.saveEntry.set_text(jE["file-text"])
        self.lbox_e.append(self.saveEntry)
        
        self.sbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.sbox.set_margin_top(9)
        self.sbox.set_margin_bottom(9)
        
        self.saveButton = Gtk.Button.new_from_icon_name("document-save-symbolic")
        self.saveButton.add_css_class("suggested-action")
        self.saveButton.add_css_class("circular")
        self.saveButton.connect("clicked", self.set_title_t)
        self.sbox.append(self.saveButton)
        
        self.adw_action_row_save = Adw.ActionRow.new()
        self.adw_action_row_save.set_title(_["save_config"])
        self.adw_action_row_save.set_title_lines(3)
        self.adw_action_row_save.add_suffix(widget=self.sbox)
        self.adw_action_row_save.set_activatable_widget(widget=self.saveButton)
        self.lbox_e.append(child=self.adw_action_row_save)
        
        self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.obox.set_margin_top(9)
        self.obox.set_margin_bottom(9)
        
        self.loadButton = Gtk.Button.new_from_icon_name("document-open-symbolic")
        self.loadButton.add_css_class("circular")
        self.loadButton.connect("clicked", self.apply_config)
        self.obox.append(self.loadButton)
        
        self.adw_action_row_load = Adw.ActionRow.new()
        self.adw_action_row_load.set_title(_["import_config"])
        self.adw_action_row_load.set_title_lines(3)
        self.adw_action_row_load.add_suffix(widget=self.obox)
        self.adw_action_row_load.set_activatable_widget(widget=self.loadButton)
        self.lbox_a.append(child=self.adw_action_row_load)
        
        self.pBox.append(self.toast_overlay)
        
    def set_title_t(self, w):
        if " " in self.saveEntry.get_text():
            self.spaces_toast()
        else:
            self.please_wait_toast()
            self.save_config()
            self.timeout_id = GLib.timeout_add_seconds(10, self.exporting_done)
    
    # Save configuration
    def save_config(self):
        if not os.path.exists("{}/SaveDesktop/".format(download_dir)):
            os.system("mkdir {}/SaveDesktop/".format(download_dir))
        if not os.path.exists("{}/SaveDesktop/archives".format(download_dir)):
            os.system("mkdir {}/SaveDesktop/archives/".format(download_dir))
        os.system("mkdir -p {}/SaveDesktop/.{} && cd {}/SaveDesktop/.{}".format(download_dir, date.today(), download_dir, date.today()))
        os.chdir('{}/SaveDesktop/.{}'.format(download_dir, date.today()))
        os.popen('cp ~/.config/dconf/user ./')
        os.popen('cp -R ~/.local/share/backgrounds ./')
        os.popen('cp -R ~/.local/share/icons ./')
        os.popen('cp -R ~/.themes ./')
        os.popen('cp -R ~/.icons ./')
        # Save configs on individual desktop environments
        if self.environment == 'GNOME':
            os.popen("cp -R ~/.local/share/gnome-background-properties ./")
            os.popen("cp -R ~/.local/share/gnome-shell ./")
            os.popen("cp -R ~/.local/share/nautilus-python ./")
            os.popen("cp -R ~/.config/gnome-control-center ./")
        elif self.environment == 'Pantheon':
            os.popen("cp -R ~/.config/plank ./")
            os.popen("cp -R ~/.config/marlin ./")
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
            os.popen("cp -R ~/.xfce4 ./")
        elif self.environment == 'MATE':
            os.popen("cp -R ~/.config/caja ./")
              
        # Get self.saveEntry text
        if self.saveEntry.get_text() == "":
            os.popen("tar --gzip -cf config_{}.sd.tar.gz ./".format(date.today()))
        else:
            os.popen("tar --gzip -cf {}.sd.tar.gz ./".format(self.saveEntry.get_text()))
        
    # Load file chooser
    def fileshooser(self):
        self.file_chooser = Gtk.FileChooserDialog()
        self.file_chooser.set_transient_for(self)
        self.file_chooser.set_title(_["import_fileshooser"].format(self.environment))
        self.file_chooser.set_action(Gtk.FileChooserAction.OPEN)
        self.file_chooser.add_buttons(_["open"], Gtk.ResponseType.ACCEPT, \
            _["cancel"], Gtk.ResponseType.CANCEL)
        self.file_chooser.set_current_folder( \
            Gio.File.new_for_path(os.environ['HOME']))
        self.file_chooser.set_modal(True)
        self.file_filter = Gtk.FileFilter.new()
        self.file_filter.set_name(_["savedesktop_f"])
        self.file_filter.add_pattern('*.sd.tar.gz')
        self.file_chooser.add_filter(self.file_filter)
        self.file_chooser.connect('response', self.open_response)
        self.file_chooser.show()
        
    ## Action after closing file chooser
    def open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            dialog.close()
            file = dialog.get_file()
            filename = file.get_path()
            self.please_wait_toast()
            self.timeout_io = GLib.timeout_add_seconds(10, self.applying_done)
            # Applying configuration for GNOME-based environments
            if not os.path.exists("{}/.config".format(Path.home())):
                os.system("mkdir ~/.config/")
            if not os.path.exists("{}/.config/dconf".format(Path.home())):
                os.system("mkdir ~/.config/dconf/")
            os.chdir("%s" % CACHE)
            os.popen("tar -xf %s ./" % filename)
            self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
        else:
            dialog.close()
            
    def import_config(self):
        os.popen("rm ~/.config/dconf/* && cp ./user ~/.config/dconf/")
        os.popen('cp -R ./icons ~/.local/share/')
        os.popen('cp -R ./.themes ~/')
        os.popen('cp -R ./.icons ~/')
        os.popen("cp -R ./backgrounds ~/.local/share/")
        # Apply configs for individual desktop environments
        if self.environment == 'GNOME':
            os.popen("cp -R ./gnome-background-properties ~/.local/share/")
            os.popen("cp -R ./gnome-shell ~/.local/share/")
            os.popen("cp -R ./nautilus-python ~/.local/share/")
            os.popen("cp -R ./gnome-control-center ~/.config/")
        elif self.environment == 'Pantheon':
            os.popen("cp -R ./plank ~/.config/")
            os.popen("cp -R ./marlin ~/.config/")
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
            os.popen("cp -R ./.xfce4 ~/")
        elif self.environment == 'MATE':
            os.popen("cp -R ./caja ~/.config/")
        #self.applying_done()
            
    ## open file chooser
    def apply_config(self, w):
        self.fileshooser()
    
    # configuration has been exported action
    def exporting_done(self):
        self.toast.set_title(title=_["config_saved"])
        self.toast.set_button_label(_["open_folder"])
        self.toast.set_action_name("app.open_dir")
        os.chdir('{}/SaveDesktop/.{}'.format(download_dir, date.today()))
        os.popen('mv ./*.tar.gz {}/SaveDesktop/archives/'.format(download_dir))
        self.toast_overlay.add_toast(self.toast)
        
    def spaces_toast(self):
        self.toast_sp = Adw.Toast(title=_["filename_spaces_msg"])
        self.toast_sp.set_timeout(5)
        self.toast_sp.connect('dismissed', self.on_toast_p_dismissed)
        self.toast_overlay.add_toast(self.toast_sp)
    
    # Config has been imported action
    def applying_done(self):
        self.toast.set_title(title=_["config_imported"])
        self.toast.set_button_label(_["logout"])
        self.toast.set_action_name("app.logout")
        self.toast_overlay.add_toast(self.toast)
        
    def please_wait_toast(self):
        self.toast_wait = Adw.Toast(title=_["please_wait"])
        self.toast_wait.set_timeout(10)
        self.toast_wait.connect('dismissed', self.on_toast_w_dismissed)
        self.toast_overlay.add_toast(self.toast_wait)
        
    def unsupp_toast(self):
        self.toast_unsupp = Adw.Toast(title=_["unsupp_file_desc"])
        self.toast_unsupp.set_timeout(5)
        self.toast_unsupp.connect('dismissed', self.on_toast_u_dismissed)
        self.toast_overlay.add_toast(self.toast_unsupp)
    
    def on_toast_dismissed(self, toast):
        print('')
        os.popen("rm -rf %s/*" % CACHE)
        os.popen("rm -rf {}/SaveDesktop/.{}/*".format(download_dir, date.today()))
    
    def on_toast_w_dismissed(self, toast_wait):
        print('')
        
    def on_toast_u_dismissed(self, toast_unsupp):
        print('')
        
    def on_toast_p_dismissed(self, toast_sp):
        print('')
    
    # Drag and drop function
    def on_drop(self, DropTarget, data, x, y):
        if tarfile.is_tarfile(data) == True:
            self.please_wait_toast()
            self.timeout_io = GLib.timeout_add_seconds(10, self.applying_done)
            # Applying configuration for GNOME-based environments
            if not os.path.exists("{}/.config".format(Path.home())):
                os.system("mkdir ~/.config/")
            if not os.path.exists("{}/.config/dconf".format(Path.home())):
                os.system("mkdir ~/.config/dconf/")
            os.chdir("%s" % CACHE)
            os.popen(f"tar -xf {data} ./")
            self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
        else:
            self.unsupp_toast()
            
    def on_prepare(self, DropTarget, x, y):
        print('')

    def on_drag_begin(self):
        print('')

    def on_drag_end(self):
        print('')

    def on_drag_cancel(self):
        print('')
        
    # Get settings from XDG_CONFIG/settings.json
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
    
    # action after closing window
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
        if lang == "en.json":
            print("")
        else:
            dialog.set_translator_credits(_["translator_credits"])
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/SaveDesktop")
        dialog.set_issue_url("https://github.com/vikdevelop/SaveDesktop")
        dialog.set_copyright("© 2023 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("io.github.vikdevelop.SaveDesktop")
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
