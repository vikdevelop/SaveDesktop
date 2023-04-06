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
# Turkish
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=tr_TR.UTF-8':
    lang = 'tr.json'
# Deutsch
elif subprocess.getoutput('locale | grep "LANG"') == 'LANG=de_DE.UTF-8':
    lang = 'de.json'
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
        
        self.savedesktop_mode_dropdwn = Gtk.DropDown.new_from_strings( \
            [_["save_config"], _["import_config"]] )
        #self.savedesktop_mode_dropdwn.get_first_child().add_css_class('flat')
        self.savedesktop_mode_dropdwn.set_tooltip_text("Select SaveDesktop page")
        self.savedesktop_mode_dropdwn.connect('notify::selected-item', \
            self.change_savedesktop_mode)
        self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
        
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
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
            self.environment = 'KDE Plasma'
            self.save_desktop()
            self.connect("close-request", self.on_close)
        else:
            self.Image = Gtk.Image.new_from_icon_name("exclamation_mark")
            self.Image.set_pixel_size(50)
            self.pBox.append(self.Image)
            self.label_sorry = Gtk.Label()
            self.label_sorry.set_markup(_["unsuppurted_env_desc"].format("GNOME, Xfce, Budgie, Cinnamon, COSMIC, Pantheon, KDE Plasma, MATE"))
            self.label_sorry.set_wrap(True)
            self.label_sorry.set_justify(Gtk.Justification.CENTER)
            self.pBox.append(self.label_sorry)
    
    def change_savedesktop_mode(self, w, pspec):
        if self.savedesktop_mode_dropdwn.get_selected() == 0:
            self.save_desktop()
        else:
            self.import_desktop()
    
    # Show main layout
    def save_desktop(self):
        # Remove Import page box
        try:
            self.pBox.remove(self.importBox)
        except:
            print("")
        # Remove controller for drag and drop if loaded save page
        try:
            self.remove_controller(self.drag_source)
            self.remove_controller(self.drop_target)
        except:
            print("")
        
        # Box for save page
        self.saveBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.pBox.append(self.saveBox)
        
        # Tittle image for save page
        self.titleImage = Gtk.Image.new_from_icon_name("desktop-symbolic")
        self.titleImage.set_pixel_size(64)
        self.saveBox.append(self.titleImage) 
        
        # Tittle "Save Current configuration" for save page and subtitle "{user_desktop}"
        self.label_title = Gtk.Label.new()
        self.label_title.set_markup('\n<big><b>{}</b></big>\n{}\n'.format(_["save_config"], self.environment))
        self.label_title.set_justify(Gtk.Justification.CENTER)
        self.saveBox.append(self.label_title)
        
        # Box for show this options: set the filename, save flatpak custom permissions and periodic saving
        self.lbox_e = Gtk.ListBox.new()
        self.lbox_e.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.lbox_e.get_style_context().add_class(class_name='boxed-list')
        self.saveBox.append(self.lbox_e)
        
        # set the filename section
        self.saveEntry = Adw.EntryRow.new()
        self.saveEntry.set_title(_["set_filename"])
        self.saveEntry.connect('changed', self.on_saveentry)
        if os.path.exists(f'{CONFIG}/settings.json'):
            with open(f'{CONFIG}/settings.json') as e:
                jE = json.load(e)
            self.saveEntry.set_text(jE["file-text"])
        self.lbox_e.append(self.saveEntry)
        
        # Switch and row of option 'Save Flatpak custom permissions'
        self.switch_01 = Gtk.Switch.new()
        if os.path.exists(f'{CONFIG}/settings.json'):
            with open(f'{CONFIG}/settings.json') as r:
                jR = json.load(r)
            try:
                flatpak = jR["save_flatpak_permissions"]
                if flatpak == "True":
                    self.switch_01.set_active(True)
                else:
                    self.switch_01.set_active(False)
            except:
                self.switch_01.set_active(False)
        else:
            self.switch_01.set_active(False)
        self.switch_01.set_valign(align=Gtk.Align.CENTER)
         
        self.adw_action_row_more = Adw.ActionRow.new()
        self.adw_action_row_more.set_title(title=_["save_flatpak_permissions"])
        self.adw_action_row_more.set_title_lines(2)
        self.adw_action_row_more.set_subtitle_lines(2)
        self.adw_action_row_more.add_suffix(self.switch_01)
        self.adw_action_row_more.set_activatable_widget(self.switch_01)
        self.lbox_e.append(child=self.adw_action_row_more)
        
        self.lbox_e.set_show_separators(True)
        
        # Periodic backups section
        actions = Gtk.StringList.new(strings=[
            _["never"], _["daily"], _["weekly"], _["monthly"]
        ])
        
        self.adw_action_row_backups = Adw.ComboRow.new()
        self.adw_action_row_backups.set_title(title=_["periodic_saving"])
        self.adw_action_row_backups.set_subtitle(subtitle=_["periodic_saving_desc"])
        self.adw_action_row_backups.set_title_lines(2)
        self.adw_action_row_backups.set_subtitle_lines(2)
        self.adw_action_row_backups.set_model(model=actions)
        self.lbox_e.append(child=self.adw_action_row_backups)
        
        if os.path.exists(f'{CONFIG}/settings.json'):
            with open(f'{CONFIG}/settings.json') as b:
                jb = json.load(b)
            try:
                if jb["periodic_backups"] == "Never":
                    self.adw_action_row_backups.set_selected(0)
                elif jb["periodic_backups"] == "Daily":
                    self.adw_action_row_backups.set_selected(1)
                elif jb["periodic_backups"] == "Weekly":
                    self.adw_action_row_backups.set_selected(2)
                elif jb["periodic_backups"] == "Monthly":
                    self.adw_action_row_backups.set_selected(3)
            except:
                self.adw_action_row_backups.set_selected(0)
        else:
            self.adw_action_row_backups.set_selected(0)
        
        self.savebtnBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.savebtnBox.set_margin_top(10)
        self.savebtnBox.set_margin_start(180)
        self.savebtnBox.set_margin_end(180)
        self.saveBox.append(self.savebtnBox)
        
        # save configuration button
        self.saveButton = Gtk.Button.new_with_label(_["save"])
        self.saveButton.add_css_class("suggested-action")
        self.saveButton.add_css_class("pill")
        self.saveButton.set_sensitive(False)
        self.saveButton.connect("clicked", self.set_title_t)
        self.savebtnBox.append(self.saveButton)
    
    def on_saveentry(self, saveEntry):
        entry = self.saveEntry.get_text()
        if entry == '':
            self.saveButton.set_sensitive(False)
        else:
            self.saveButton.set_sensitive(True)
        
    # Import configuration section
    def import_desktop(self):
        try:
            self.pBox.remove(self.saveBox)
        except:
            print("")
        
        # Drag and drop area
        self.drag_source = Gtk.DragSource.new()
        self.drag_source.set_actions(Gdk.DragAction.COPY)

        self.drop_target = Gtk.DropTarget.new(GObject.TYPE_STRING, Gdk.DragAction.COPY)
        self.drop_target.connect('drop', self.on_drop)

        self.add_controller(self.drag_source)
        self.add_controller(self.drop_target)
        
        # box for import page
        self.importBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Image for import page
        self.importImage = Gtk.Image.new_from_icon_name("document-open-symbolic")
        self.importImage.set_pixel_size(64)
        self.importBox.append(self.importImage)
        
        # Title and subtitle for import page 
        self.labelImport = Gtk.Label.new()
        self.labelImport.set_markup(f"<big><b>{_['import_config']}</b></big>")
        self.importBox.append(self.labelImport)
        
        self.labelDesc = Gtk.Label.new(str=_["import_config_desc"])
        self.importBox.append(self.labelDesc)
        
        # Box of this buttons: Import from file and Import from list
        self.importbtnBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.importbtnBox.set_halign(Gtk.Align.CENTER)
        self.importBox.append(self.importbtnBox)
        
        # Import configuration button
        self.fileButton = Gtk.Button.new_with_label(_["import_from_file"])
        self.fileButton.add_css_class("pill")
        self.fileButton.add_css_class("suggested-action")
        self.fileButton.connect("clicked", self.apply_config)
        self.importbtnBox.append(self.fileButton)
        
        # Import from list button
        self.fromlistButton = Gtk.Button.new_with_label(_["import_from_list"])
        self.fromlistButton.add_css_class("pill")
        self.fromlistButton.connect("clicked", self.import_from_list)
        self.importbtnBox.append(self.fromlistButton)
        
        self.pBox.append(self.importBox)
        
    # Import archive from list
    def import_from_list(self, w):
        self.pBox.remove(self.importBox)
        self.backButton = Gtk.Button.new_from_icon_name("go-next-symbolic-rtl")
        self.backButton.add_css_class("flat")
        self.backButton.connect("clicked", self.close_list)
        self.headerbar.remove(self.savedesktop_mode_dropdwn)
        self.headerbar.pack_start(self.backButton)
        
        self.flistBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.pBox.append(self.flistBox)
        
        self.flistLabel = Gtk.Label.new()
        self.flistBox.append(self.flistLabel)
        if not os.path.exists(f'{download_dir}/SaveDesktop/archives/'):
            self.flistLabel.set_text(_["import_from_list_error"])
        if os.listdir(f'{download_dir}/SaveDesktop/archives/') == []:
            self.flistLabel.set_text(_["import_from_list_error"])
        else:
            self.flistLabel.set_markup(f"<big><b>{_['import_from_list']}</b></big>")
            self.fdesclabel = Gtk.Label.new(f"{download_dir}/SaveDesktop/archives")
            self.flistBox.append(self.fdesclabel)
            
            self.applyButton = Gtk.Button.new_with_label(_["apply"])
            self.applyButton.add_css_class('suggested-action')
            self.applyButton.connect('clicked', self.imp_cfg_from_list)
            self.headerbar.pack_end(self.applyButton)
            
            self.radioBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            self.listbox = Gtk.ListBox.new()
            self.listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
            self.listbox.get_style_context().add_class(class_name='boxed-list')
            self.flistBox.append(self.listbox)
            
            get_dir_content = os.listdir(f'{download_dir}/SaveDesktop/archives')
            archives_model = Gtk.StringList.new(strings=get_dir_content)
            
            self.radio_row = Adw.ComboRow.new()
            self.radio_row.set_model(model=archives_model)
            self.radio_row.set_icon_name('document-properties-symbolic')
            self.listbox.append(self.radio_row)
        
    # Action after closing import from list page
    def close_list(self, w):
        self.pBox.append(self.importBox)
        self.pBox.remove(self.flistBox)
        self.headerbar.remove(self.backButton)
        self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
        try:
            self.headerbar.remove(self.applyButton)
        except:
            print("")
        
    # Import config from list
    def imp_cfg_from_list(self, w):
        selected_archive = self.radio_row.get_selected_item()
        self.please_wait_toast()
        self.timeout_io = GLib.timeout_add_seconds(10, self.applying_done)
        os.chdir("%s" % CACHE)
        os.popen("tar -xf %s/SaveDesktop/archives/%s ./" % (download_dir, selected_archive.get_string()))
        self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
    
    # Check if filename has spaces or not
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
        os.popen('cp -R ~/.fonts ./')
        os.popen('cp -R ~/.config/gtk-4.0 ./')
        os.popen('cp -R ~/.config/gtk-3.0 ./')
        if self.switch_01.get_active() == True:
            os.popen('cp -R ~/.local/share/flatpak/overrides ./')
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
        elif self.environment == 'KDE Plasma':
            os.system("mkdir xdg-config && mkdir xdg-data")
            os.popen("cp -R ~/.config/[k]* ./xdg-config/")
            os.popen("cp ~/.config/gtkrc ./xdg-config/")
            os.popen("cp ~/.config/dolphinrc ./xdg-config/")
            os.popen("cp ~/.config/gwenviewrc ./xdg-config/")
            os.popen("cp ~/.config/plasmashellrc ./xdg-config/")
            os.popen("cp ~/.config/spectaclerc ./xdg-config/")
            os.popen("cp ~/.config/plasmarc ./xdg-config/")
            os.popen("cp -R ~/.local/share/[k]* ./xdg-data/")
            os.popen("cp -R ~/.local/share/dolphin ./xdg-data/")
            os.popen("cp -R ~/.local/share/sddm ./xdg-data/")
            os.popen("cp -R ~/.local/share/wallpapers ./xdg-data/")
            os.popen("cp -R ~/.local/share/plasma-systemmonitor ./xdg-data/")
            os.popen("cp -R ~/.local/share/plasma ./xdg-data/")
            os.popen("cp -R ~/.local/share/aurorae ./xdg-data/")
            os.popen("cp -R ~/.local/share/color-schemes ./xdg-data/")
              
        # Get self.saveEntry text
        if self.saveEntry.get_text() == "":
            os.popen("tar --gzip -cf config_{}.sd.tar.gz ./".format(date.today()))
        else:
            os.popen("tar --gzip -cf {}.sd.tar.gz ./".format(self.saveEntry.get_text()))
    
    # Load file chooser
    def fileshooser(self):
        self.file_chooser = Gtk.FileChooserNative.new(_["import_fileshooser"].format(self.environment), \
                self, Gtk.FileChooserAction.OPEN, _["open"], _["cancel"])
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
            file = dialog.get_file()
            filename = file.get_path()
            self.please_wait_toast()
            self.timeout_io = GLib.timeout_add_seconds(10, self.applying_done)
            os.chdir("%s" % CACHE)
            os.popen("tar -xf %s ./" % filename)
            self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
            
    # Import configuration
    def import_config(self):
        # Applying configuration for GNOME-based environments
        if not os.path.exists("{}/.config".format(Path.home())):
            os.system("mkdir ~/.config/")
        if not os.path.exists("{}/.config/dconf".format(Path.home())):
            os.system("mkdir ~/.config/dconf/")
        os.popen("rm ~/.config/dconf/* && cp ./user ~/.config/dconf/")
        os.popen('cp -R ./icons ~/.local/share/')
        os.popen('cp -R ./.themes ~/')
        os.popen('cp -R ./.icons ~/')
        os.popen("cp -R ./backgrounds ~/.local/share/")
        os.popen('cp -R ./.fonts ~/')
        os.popen('cp -R ./gtk-4.0 ~/.config/')
        os.popen('cp -R ./gtk-3.0 ~/.config/')
        os.popen('cp -R ./overrides ~/.local/share/flatpak/')
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
        elif self.environment == 'KDE Plasma':
            os.popen("cp -R ./xdg-config/* ~/.config/")
            os.popen("cp -R ./xdg-data/* ~/.local/share/")
            
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
        
    # popup about message of using spaces in the filename
    def spaces_toast(self):
        self.toast_sp = Adw.Toast(title=_["filename_spaces_msg"])
        self.toast_sp.set_timeout(5)
        self.toast_overlay.add_toast(self.toast_sp)
    
    # Config has been imported action
    def applying_done(self):
        self.toast.set_title(title=_["config_imported"])
        self.toast.set_button_label(_["logout"])
        self.toast.set_action_name("app.logout")
        self.toast_overlay.add_toast(self.toast)
        
    # popup about message "Please wait ..."
    def please_wait_toast(self):
        self.toast_wait = Adw.Toast(title=_["please_wait"])
        self.toast_wait.set_timeout(10)
        self.toast_overlay.add_toast(self.toast_wait)
       
    # Popup about unsupported file
    def unsupp_toast(self):
        self.toast_unsupp = Adw.Toast(title=_["unsupp_file_desc"])
        self.toast_unsupp.set_timeout(5)
        self.toast_overlay.add_toast(self.toast_unsupp)
        
    # Popup about unable to find the file
    def fileerr_toast(self):
        self.toast_fileerr = Adw.Toast(title=_["unable_find_file"])
        self.toast_fileerr.set_timeout(7)
        self.toast_overlay.add_toast(self.toast_fileerr)
    
    def on_toast_dismissed(self, toast):
        os.popen("rm -rf %s/*" % CACHE)
        os.popen("rm -rf {}/SaveDesktop/.{}/*".format(download_dir, date.today()))
    
    # Drag and drop function
    def on_drop(self, DropTarget, data, x, y):
        if os.path.exists(data):
            if "sd.tar.gz" in data:
                self.please_wait_toast()
                self.timeout_io = GLib.timeout_add_seconds(10, self.applying_done)
                os.chdir("%s" % CACHE)
                os.popen(f"tar -xf {data} ./")
                self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
            else:
                self.unsupp_toast()
        else:
            self.fileerr_toast()
        
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
        selected_item = self.adw_action_row_backups.get_selected_item()
        # Create desktop file to make periodic backups work
        if selected_item.get_string() == _["never"]:
            backup_item = "Never"
        else:
            if not os.path.exists(f'{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop'):
                with open(f'{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop', 'w') as cb:
                    cb.write('[Desktop Entry]\nName=SaveDesktop (Periodic backups)\nType=Application\nExec=flatpak run io.github.vikdevelop.SaveDesktop --background')
        # Translate backup items to English because it is necessary for the proper functioning of periodic backups correctly
        if selected_item.get_string() == _["daily"]:
            backup_item = "Daily"
        if selected_item.get_string() == _["weekly"]:
            backup_item = "Weekly"
        if selected_item.get_string() == _["monthly"]:
            backup_item = "Monthly"
        # Save settings of filename text, periodic backups and window size
        with open(f'{CONFIG}/settings.json', 'w') as s:
            s.write('{\n "file-text": "%s",\n "periodic_backups": "%s",\n "save_flatpak_permissions": "%s",\n "window_width": "%s",\n "window_height": "%s"\n}' % (self.saveEntry.get_text(), backup_item, self.switch_01.get_active(), self.get_allocation().width, self.get_allocation().height))
        
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
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
            os.system("dbus-send --print-reply --dest=org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout int32:0 int32:0 int32:0")
        else:
            os.system("dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1")
        
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("SaveDesktop")
        dialog.set_version("2.2")
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
