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
if "cs" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'cs.json'
# French
elif "fr" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'fr.json'
# Portugalese (Brasil)    
elif "pt_BR" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'pt_BR.json'
# Italian    
elif "it" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'it.json'
# Dutch
elif "nl" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'nl.json'
# Arabic
elif "ar" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'ar.json'
# Russian
elif "ru" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'ru.json'
# Indonesian
elif "id" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'id.json'
# Norwegian (Bokmål)
elif "nb_NO" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'nb_NO.json'
# Ukrainian
elif "uk" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'uk.json'
# Hungarian
elif "hu" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'hu.json'
# Spanish
elif "es" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'es.json'
# Turkish
elif "tr" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'tr.json'
# Deutsch
elif "de" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'de.json'
# Chinese (Simplified)
elif "zh" in subprocess.getoutput('locale | grep "LANG"'):
    lang = 'zh_Hans.json'
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
        self.savedesktop_mode_dropdwn.connect('notify::selected-item', \
            self.change_savedesktop_mode)
        
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
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'zorin:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'ubuntu:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
            self.environment = 'COSMIC'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Pantheon':
            self.environment = 'Pantheon'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'X-Cinnamon':
            self.environment = 'Cinnamon'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Budgie:GNOME':
            self.environment = 'Budgie'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
            self.environment = 'Xfce'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'MATE':
            self.environment = 'MATE'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
            self.environment = 'KDE Plasma'
            self.save_desktop()
            self.headerbar.pack_start(self.savedesktop_mode_dropdwn)
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
        self.lbox_e.add_css_class(css_class='boxed-list')
        self.saveBox.append(self.lbox_e)
        
        # set the filename section
        self.saveEntry = Adw.EntryRow.new()
        self.saveEntry.set_title(_["set_filename"])
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
        self.adw_action_row_more.set_subtitle_lines(3)
        self.adw_action_row_more.add_suffix(self.switch_01)
        self.adw_action_row_more.set_activatable_widget(self.switch_01)
        self.lbox_e.append(child=self.adw_action_row_more)
        
        self.lbox_e.set_show_separators(True)
        
        # Periodic backups section
        actions = Gtk.StringList.new(strings=[
            _["never"], _["daily"], _["weekly"], _["monthly"]
        ])
        
        self.periodicButton = Gtk.Button.new_from_icon_name("folder-open-symbolic")
        self.periodicButton.add_css_class("flat")
        self.periodicButton.connect("clicked", self.open_periodic_backups)
        self.periodicButton.set_tooltip_text(_["periodic_saving_tooltip"])
        
        self.adw_action_row_backups = Adw.ComboRow.new()
        if os.path.exists(f"{download_dir}/SaveDesktop/archives"):
            self.adw_action_row_backups.add_suffix(self.periodicButton)
        self.adw_action_row_backups.set_use_markup(True)
        self.adw_action_row_backups.set_use_underline(True)
        self.adw_action_row_backups.set_title(_["periodic_saving"])
        self.adw_action_row_backups.set_subtitle(f"{_['periodic_saving_desc']}\n<a href='https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving'>{_['learn_more']}</a>")
        self.adw_action_row_backups.set_title_lines(2)
        self.adw_action_row_backups.set_subtitle_lines(4)
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
        self.saveButton.connect("clicked", self.select_folder)
        self.savebtnBox.append(self.saveButton)
        
    # Import configuration section
    def import_desktop(self):
        try:
            self.pBox.remove(self.saveBox)
        except:
            print("")
        
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
        self.flistLabel.set_justify(Gtk.Justification.CENTER)
        self.flistBox.append(self.flistLabel)
        if os.path.exists(f'{download_dir}/SaveDesktop/archives'):
            if os.listdir(f'{download_dir}/SaveDesktop/archives') == []:
                self.flistLabel.set_text(_["import_from_list_error"])
            else:
                self.flistLabel.set_markup(f"<big><b>{_['import_from_list']}</b></big>")
                self.fdescLabel = Gtk.Label.new(str=f"{download_dir}/SaveDesktop/archives")
                self.flistBox.append(self.fdescLabel)
        
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

        else:
            self.flistLabel.set_text(_["import_from_list_error"])
    
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
        os.chdir("%s" % CACHE)
        os.popen("tar -xf %s/SaveDesktop/archives/%s ./" % (download_dir, selected_archive.get_string()))
        self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
        
    def open_periodic_backups(self, w):
        os.system(f"xdg-open {download_dir}/SaveDesktop/archives")
    
    # Save configuration
    def save_config(self):
        # Create and load directory for saving configuration in CACHE
        if not os.path.exists(f"{CACHE}/saved_config"):
            os.mkdir(f"{CACHE}/saved_config")
        os.chdir(f"{CACHE}/saved_config")
        self.dconf = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/dconf/user ./")
        self.backgrounds = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/backgrounds ./")
        self.themes = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.themes ./")
        self.icons = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.icons ./")
        self.icons = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/icons ./")
        self.fonts = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.fonts ./")
        self.gtk4 = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/gtk-4.0 ./")
        self.gtk3 = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/gtk-3.0 ./")
        if self.switch_01.get_active() == True:
            self.overrides = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/flatpak/overrides ./")
        # Save configs on individual desktop environments
        if self.environment == 'GNOME':
            self.background_properties = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/gnome-background-properties ./")
            self.gshell = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/gnome-shell ./")
            self.nautilus = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/nautilus-python ./")
            self.gccenter = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/gnome-control-center ./")
        elif self.environment == 'Pantheon':
            self.plank = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/plank ./")
            self.marlin = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/marlin ./")
        elif self.environment == 'Cinnamon':
            self.nemo = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/nemo ./")
            self.data_cinn = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/cinnamon ./")
            self.home_cinn = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.cinnamon ./")
        elif self.environment == 'Budgie':
            self.budgie_desktop = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/budgie-desktop ./")
            self.budgie_extras = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/bugie-extras ./")
            self.nemo_budgie = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/nemo ./")
        elif self.environment == 'COSMIC':
            self.pop_shell = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/pop-shell ./")
            self.gshellpop = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/gnome-shell ./")
        elif self.environment == 'Xfce':
            self.xfce4conf = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/xfce4 ./")
            self.thunarxf = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/Thunar ./")
            self.xfce4home = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.xfce4 ./")
        elif self.environment == 'MATE':
            self.caja_mate = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/caja ./")
        elif self.environment == 'KDE Plasma':
            os.system("mkdir xdg-config && mkdir xdg-data")
            os.popen(f"cp -R ~/.config/[k]* ./xdg-config/")
            self.gtkrc = GLib.spawn_command_line_async(f"cp {Path.home()}/.config/gtkrc ./xdg-config/")
            self.dolphinrc = GLib.spawn_command_line_async(f"cp {Path.home()}/.config/dolphinrc ./xdg-config/")
            self.gwenviewrc = GLib.spawn_command_line_async(f"cp {Path.home()}/.config/gwenviewrc ./xdg-config/")
            self.plasmashrc = GLib.spawn_command_line_async(f"cp {Path.home()}/.config/plasmashellrc ./xdg-config/")
            self.spectaclerc = GLib.spawn_command_line_async(f"cp {Path.home()}/.config/spectaclerc ./xdg-config/")
            self.plasmarc = GLib.spawn_command_line_async(f"cp {Path.home()}/.config/plasmarc ./xdg-config/")
            self.kpanel = GLib.spawn_command_line_async(f"cp {Path.home()}/.config/plasma-org.kde.plasma.desktop-appletsrc ./xdg-config/")
            self.kdata = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/konsole ./xdg-data/")
            self.dolphin_data = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/dolphin ./xdg-data/")
            self.sddm = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/sddm ./xdg-data/")
            self.wallpapers = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/wallpapers ./xdg-data/")
            self.psysmonitor = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/plasma-systemmonitor ./xdg-data/")
            self.plasma_data = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/plasma ./xdg-data/")
            self.aurorae = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/aurorae ./xdg-data/")
            self.kscreen = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/kscreen ./xdg-data/")
            self.colors = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/color-schemes ./xdg-data/")
              
        # Get self.saveEntry text
        if self.saveEntry.get_text() == "":
            self.create_classic_tar = GLib.spawn_command_line_async(f"tar --gzip -cf config_{date.today()}.sd.tar.gz ./")
        else:
            self.create_classic_tar = GLib.spawn_command_line_async(f"tar -czf {self.saveEntry.get_text()}.sd.tar.gz ./")
        self.tar_time = GLib.timeout_add_seconds(4, self.exporting_done)
        
    # Select folder for saving configuration
    def select_folder(self, w):
        def save_selected(source, res, data):
            try:
                file = source.select_folder_finish(res)
            except:
                return
            self.please_wait_toast()
            self.folder = file.get_path()
            with open(f"{CACHE}/.filedialog.json", "w") as fd:
                fd.write('{\n "recently_folder": "%s"\n}' % self.folder)
            self.save_config()
        
        if " " in self.saveEntry.get_text():
            self.spaces_toast()
        else:
            self.folderchooser = Gtk.FileDialog.new()
            self.folderchooser.set_modal(True)
            self.folderchooser.set_title(_["save_config"])
            self.folderchooser.select_folder(self, None, save_selected, None)
            
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
        os.popen('rm ~/.config/dconf/user')
        self.i_dconf = GLib.spawn_command_line_async(f"cp ./user {Path.home()}/.config/dconf/")
        self.i_icons = GLib.spawn_command_line_async(f'cp -R ./icons {Path.home()}/.local/share/')
        self.i_themes = GLib.spawn_command_line_async(f'cp -R ./.themes {Path.home()}/')
        self.i_icons_home = GLib.spawn_command_line_async(f'cp -R ./.icons {Path.home()}/')
        self.i_backgrounds = GLib.spawn_command_line_async(f'cp -R ./backgrounds {Path.home()}/.local/share/')
        self.i_fonts = GLib.spawn_command_line_async(f'cp -R ./.fonts {Path.home()}/')
        self.i_gtk4 = GLib.spawn_command_line_async(f'cp -R ./gtk-4.0 {Path.home()}/.config/')
        self.i_gtk3 = GLib.spawn_command_line_async(f'cp -R ./gtk-3.0 {Path.home()}/.config/')
        self.i_overrides = GLib.spawn_command_line_async(f'cp -R ./overrides {Path.home()}/.local/share/flatpak/')
        # Apply configs for individual desktop environments
        if self.environment == 'GNOME':
            self.i_background_properties = GLib.spawn_command_line_async(f'cp -R ./gnome-background-properties {Path.home()}/.local/share/')
            self.i_gshell = GLib.spawn_command_line_async(f'cp -R ./gnome-shell {Path.home()}/.local/share/')
            self.i_nautilus = GLib.spawn_command_line_async(f'cp -R ./nautilus-python {Path.home()}/.local/share/')
            self.i_gccenter = GLib.spawn_command_line_async(f'cp -R ./gnome-control-center {Path.home()}/.config/')
        elif self.environment == 'Pantheon':
            self.i_plank = GLib.spawn_command_line_async(f'cp -R ./plank {Path.home()}/.config/')
            self.i_marlin = GLib.spawn_command_line_async(f'cp -R ./marlin {Path.home()}/.config/')
        elif self.environment == 'Cinnamon':
            self.i_nemo = GLib.spawn_command_line_async(f'cp -R ./nemo {Path.home()}/.config/')
            self.i_cinnamon_data = GLib.spawn_command_line_async(f'cp -R ./cinnamon {Path.home()}/.local/share/')
            self.i_cinnamon_home = GLib.spawn_command_line_async(f'cp -R ./.cinnamon {Path.home()}/')
        elif self.environment == 'Budgie':
            self.i_budgie_desktop = GLib.spawn_command_line_async(f'cp -R ./budgie-desktop {Path.home()}/.config/')
            self.i_budgie_extras = GLib.spawn_command_line_async(f'cp -R ./budgie-extras {Path.home()}/.config/')
            GLib.spawn_command_line_async(f'cp -R ./nemo {Path.home()}/.config/')
        elif self.environment == 'COSMIC':
            self.i_popshell = GLib.spawn_command_line_async(f'cp -R ./pop-shell {Path.home()}/.config/')
            self.i_gshell_pop = GLib.spawn_command_line_async(f'cp -R ./gnome-shell {Path.home()}/.local/share/')
        elif self.environment == 'Xfce':
            self.i_xfconf = GLib.spawn_command_line_async(f'cp -R ./xfce4 {Path.home()}/.config/')
            self.i_thunar = GLib.spawn_command_line_async(f'cp -R ./Thunar {Path.home()}/.config/')
            self.i_xfhome = GLib.spawn_command_line_async(f'cp -R ./.xfce4 {Path.home()}/')
        elif self.environment == 'MATE':
            self.i_caja = GLib.spawn_command_line_async(f'cp -R ./caja {Path.home()}/.config/')
        elif self.environment == 'KDE Plasma':
            os.chdir("%s" % CACHE)
            os.chdir('xdg-config')
            self.i_kconf = GLib.spawn_command_line_async(f'cp -R ./ {Path.home()}/.config/')
            os.chdir("%s" % CACHE)
            os.chdir('xdg-data')
            self.i_kdata = GLib.spawn_command_line_async(f'cp -R ./ {Path.home()}/.local/share/')
        self.applying_done()
            
    ## open file chooser
    def apply_config(self, w):
        self.fileshooser()
    
    # configuration has been exported action
    def exporting_done(self):
        os.chdir(f"{CACHE}/saved_config")
        os.system(f"mv *.tar.gz {self.folder}/")
        self.toast.set_title(title=_["config_saved"])
        self.toast.set_button_label(_["open_folder"])
        self.toast.set_action_name("app.open_dir")
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
        self.toast_overlay.add_toast(self.toast_wait)
    
    def on_toast_dismissed(self, toast):
        os.popen("rm -rf %s/*" % CACHE)
        os.popen("rm -rf {}/SaveDesktop/.{}/*".format(download_dir, date.today()))
        
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
        with open(f"{CACHE}/.filedialog.json") as fd:
            jf = json.load(fd)
        os.system("xdg-open {}/".format(jf["recently_folder"]))
        
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
        dialog.set_artists(["Brage Fuglseth"])
        version = "2.4"
        icon = "io.github.vikdevelop.SaveDesktop"
        if os.path.exists("/app/share/build-beta.sh"):
            dialog.set_version(f"{version}-beta")
            dialog.set_application_icon(f"{icon}.Devel")
        else:
            dialog.set_version(version)
            dialog.set_application_icon(icon)
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
