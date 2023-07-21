#!/usr/bin/python3
import os
import subprocess
import gi
import glob
import sys
import json
import locale
import filecmp
from datetime import date
from pathlib import Path
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk, GObject

# Load system language
p_lang = locale.getlocale()[0]
if p_lang == 'pt_BR':
    r_lang = 'pt_BR'
elif p_lang == 'nb_NO':
    r_lang = 'nb_NO'
elif 'zh' in p_lang:
    r_lang = 'zh_Hans'
else:
    r_lang = p_lang[:-3]

download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
flatpak = os.path.exists("/.flatpak-info")

if flatpak:
    try:
        locale = open(f"/app/translations/{r_lang}.json")
    except:
        locale = open(f"/app/translations/en.json")
    system_dir = "/app"
    CACHE = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/cache/tmp"
    DATA = f"{Path.home()}/.var/app/io.github.vikdevelop.SaveDesktop/data"
else:
    try:
        locale = open(f"translations/{r_lang}.json")
    except:
        locale = open("translations/en.json")
    system_dir = f"{Path.home()}/.local/share/savedesktop/src"
    os.system("mkdir ~/.cache/io.github.vikdevelop.SaveDesktop")
    os.system("mkdir ~/.local/share/io.github.vikdevelop.SaveDesktop")
    CACHE = f"{Path.home()}/.cache/io.github.vikdevelop.SaveDesktop"
    DATA = f"{Path.home()}/.local/share/io.github.vikdevelop.SaveDesktop"
    os.system(f"wget -qO {DATA}/main_window.py https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/src/main_window.py")
    result = filecmp.cmp(f"{DATA}/main_window.py", f"{Path.home()}/.local/share/savedesktop/src/main_window.py")
    if result == False:
        os.popen(f"cp {DATA}/main_window.py {Path.home()}/.local/share/savedesktop/src/")
        python = sys.executable
        os.execl(python, python, *sys.argv)

_ = json.load(locale)

class MainWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("SaveDesktop")
        self.headerbar = Adw.HeaderBar.new()
        self.set_titlebar(titlebar=self.headerbar)
        self.application = kwargs.get('application')
        
        self.settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
        
        #self.set_size_request(750, 540)
        (width, height) = self.settings["window-size"]
        self.set_default_size(width, height)
        
        if self.settings["maximized"]:
            self.maximize()
        
        # App menu
        self.menu_button_model = Gio.Menu()
        self.menu_button_model.append(_["about_app"], 'app.about')
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.menu_button_model)
        self.headerbar.pack_end(child=self.menu_button)
        
        # Primary layout
        self.headapp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.headapp.set_valign(Gtk.Align.CENTER)
        self.headapp.set_halign(Gtk.Align.CENTER)
        
        # Layout for import from list section
        self.pBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.pBox.set_halign(Gtk.Align.CENTER)
        self.pBox.set_valign(Gtk.Align.CENTER)
        
        # Stack
        self.stack =Adw.ViewStack(vexpand=True)
        self.headapp.append(self.stack)
        
        # Layout for saving and importing configuration
        self.saveBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.importBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.imp_cfg_title = _["import_from_file"]
        
        # Add pages
        self.stack.add_titled_with_icon(self.saveBox,"savepage",_["save"],"document-save-symbolic")
        self.stack.add_titled_with_icon(self.importBox,"importpage","Import","document-open-symbolic")
        
        # Adw Switcher
        self.switcher_title=Adw.ViewSwitcherTitle()
        self.switcher_title.set_stack(self.stack)
        self.switcher_title.set_title("")
        self.headerbar.set_title_widget(self.switcher_title)
        
        # Toast
        self.toast_overlay = Adw.ToastOverlay.new()
        self.toast_overlay.set_margin_top(margin=1)
        self.toast_overlay.set_margin_end(margin=1)
        self.toast_overlay.set_margin_bottom(margin=1)
        self.toast_overlay.set_margin_start(margin=1)
        
        self.set_child(self.toast_overlay)
        self.toast_overlay.set_child(self.headapp)
        
        self.toast = Adw.Toast.new(title='')
        self.toast.set_timeout(5)
        self.toast.connect('dismissed', self.on_toast_dismissed)
        
        # check of user current desktop
        if os.getenv('XDG_CURRENT_DESKTOP') == 'GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'zorin:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'ubuntu:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
            self.environment = 'COSMIC'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Pantheon':
            self.environment = 'Pantheon'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'X-Cinnamon':
            self.environment = 'Cinnamon'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Budgie:GNOME':
            self.environment = 'Budgie'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
            self.environment = 'Xfce'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'MATE':
            self.environment = 'MATE'
            self.save_desktop()
            self.import_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
            self.environment = 'KDE Plasma'
            self.save_desktop()
            self.import_desktop()
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
    
    # Show main layout
    def save_desktop(self):
        # Set margin for save desktop layout
        self.saveBox.set_margin_start(40)
        self.saveBox.set_margin_end(40)
        
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
        self.saveEntry.set_text(self.settings["filename"])
        self.lbox_e.append(self.saveEntry)
        
        # Switch and row of option 'Save Flatpak custom permissions'
        self.switch_01 = Gtk.Switch.new()
        if self.settings["save-installed-flatpaks"]:
            self.switch_01.set_active(True)
        self.switch_01.set_valign(align=Gtk.Align.CENTER)
         
        self.flatpak_row = Adw.ActionRow.new()
        self.flatpak_row.set_title(title=_["save_installed_flatpaks"])
        self.flatpak_row.set_subtitle(f'<a href="https://github.com/vikdevelop/SaveDesktop/wiki/Save-installed-Flatpak-apps-and-install-it-from-list">{_["learn_more"]}</a>')
        self.flatpak_row.set_use_markup(True)
        self.flatpak_row.set_title_lines(2)
        self.flatpak_row.set_subtitle_lines(3)
        self.flatpak_row.add_suffix(self.switch_01)
        self.flatpak_row.set_activatable_widget(self.switch_01)
        self.lbox_e.append(child=self.flatpak_row)
        
        self.lbox_e.set_show_separators(True)
        
        # Periodic backups section
        actions = Gtk.StringList.new(strings=[
            _["never"], _["daily"], _["weekly"], _["monthly"]
        ])
        
        self.periodicButton = Gtk.Button.new_from_icon_name("preferences-system-symbolic")
        self.periodicButton.add_css_class("flat")
        self.periodicButton.set_tooltip_text(_["set_pb_folder_tooltip"])
        self.periodicButton.connect("clicked", self.open_periodic_backups)
        
        self.adw_action_row_backups = Adw.ComboRow.new()
        self.adw_action_row_backups.add_suffix(self.periodicButton)
        self.adw_action_row_backups.set_use_markup(True)
        self.adw_action_row_backups.set_use_underline(True)
        self.adw_action_row_backups.set_title(_["periodic_saving"])
        self.adw_action_row_backups.set_subtitle(f"{_['periodic_saving_desc']}\n<a href='https://github.com/vikdevelop/SaveDesktop/wiki/Periodic-saving'>{_['learn_more']}</a>")
        self.adw_action_row_backups.set_title_lines(2)
        self.adw_action_row_backups.set_subtitle_lines(4)
        self.adw_action_row_backups.set_model(model=actions)
        self.lbox_e.append(child=self.adw_action_row_backups)
        
        if self.settings["periodic-saving"] == 'Never':
            self.adw_action_row_backups.set_selected(0)
        elif self.settings["periodic-saving"] == 'Daily':
            self.adw_action_row_backups.set_selected(1)
        elif self.settings["periodic-saving"] == 'Weekly':
            self.adw_action_row_backups.set_selected(2)
        elif self.settings["periodic-saving"] == 'Monthly':
            self.adw_action_row_backups.set_selected(3)
        
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
        self.importBox.set_valign(Gtk.Align.CENTER)
        self.importBox.set_halign(Gtk.Align.CENTER)
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
        self.importbtnBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=7)
        self.importbtnBox.set_halign(Gtk.Align.CENTER)
        self.importBox.append(self.importbtnBox)
        
        # Import configuration button
        self.fileButton = Gtk.Button.new_with_label(_["import_from_file"])
        self.fileButton.add_css_class("pill")
        self.fileButton.add_css_class("suggested-action")
        self.fileButton.connect("clicked", self.select_import_folder)
        self.importbtnBox.append(self.fileButton)
        
        # Import from list button
        self.fromlistButton = Gtk.Button.new_with_label(_["import_from_list"])
        self.fromlistButton.add_css_class("pill")
        self.fromlistButton.connect("clicked", self.import_from_list)
        self.importbtnBox.append(self.fromlistButton)
        
        #self.pBox.append(self.importBox)
        
    # Import archive from list
    def import_from_list(self, w):
        self.set_child(self.pBox)
        self.backButton = Gtk.Button.new_from_icon_name("go-next-symbolic-rtl")
        self.backButton.add_css_class("flat")
        self.backButton.connect("clicked", self.close_list)
        self.headerbar.set_title_widget(None)
        self.headerbar.pack_start(self.backButton)
        
        self.flistBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.pBox.append(self.flistBox)
        
        self.flistLabel = Gtk.Label.new()
        self.flistLabel.set_justify(Gtk.Justification.CENTER)
        if self.settings["periodic-saving-folder"] == '':
            self.dir = f'{download_dir}/SaveDesktop/archives'
        else:
            self.dir = f'{self.settings["periodic-saving-folder"]}'
        if os.path.exists(self.dir):
            if glob.glob(f"{self.dir}/*.sd.tar.gz") == []:
                self.flistLabel.set_text(_["import_from_list_error"])
                self.flistBox.append(self.flistLabel)
            else:
                self.flistImage = Gtk.Image.new_from_icon_name("list-view")
                self.flistImage.set_pixel_size(128)
                self.flistBox.append(self.flistImage)
                self.flistBox.append(self.flistLabel)
                
                self.flistLabel.set_markup(f"<big><b>{_['import_from_list']}</b></big>")
        
                self.applyButton = Gtk.Button.new_with_label(_["apply"])
                self.applyButton.add_css_class('suggested-action')
                self.applyButton.connect('clicked', self.imp_cfg_from_list)
                self.headerbar.pack_end(self.applyButton)
                
                self.radioBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                self.listbox = Gtk.ListBox.new()
                self.listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
                self.listbox.get_style_context().add_class(class_name='boxed-list')
                self.flistBox.append(self.listbox)
                
                self.dir_row = Adw.ActionRow.new()
                self.dir_row.set_title(_["pb_folder"])
                self.dir_row.set_subtitle(self.dir)
                self.dir_row.set_icon_name("folder-open-symbolic")
                self.listbox.append(self.dir_row)
                
                os.chdir(self.dir)
                get_dir_content = glob.glob(f"*.sd.tar.gz")
                archives_model = Gtk.StringList.new(strings=get_dir_content)

                self.radio_row = Adw.ComboRow.new()
                self.radio_row.set_model(model=archives_model)
                self.radio_row.set_icon_name('document-properties-symbolic')
                self.listbox.append(self.radio_row)
        else:
            self.flistLabel.set_text(_["import_from_list_error"])
            self.flistBox.append(self.flistLabel)
    
    # Action after closing import from list page
    def close_list(self, w):
        self.pBox.remove(self.flistBox)
        self.set_child(self.toast_overlay)
        self.toast_overlay.set_child(self.headapp)
        self.headerbar.remove(self.backButton)
        self.headerbar.set_title_widget(self.switcher_title)
        try:
            self.headerbar.remove(self.applyButton)
        except:
            print("")
        
    # Set custom folder for periodic saving dialog
    def open_periodic_backups(self, w):
        self.dirdialog()
        
    # Dialog for changing directory for periodic backups
    def dirdialog(self):
        self.dirDialog = Adw.MessageDialog.new(app.get_active_window())
        self.dirDialog.set_heading(_["set_pb_folder_tooltip"])
        self.dirLBox = Gtk.ListBox.new()
        self.dirLBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.dirLBox.get_style_context().add_class(class_name='boxed-list')
        self.dirRow = Adw.ActionRow.new()
        self.dirRow.set_title(_["pb_folder"])
        self.dirRow.set_use_markup(True)
        if self.settings["periodic-saving-folder"] == '':
            self.dirRow.set_subtitle(f"{download_dir}/SaveDesktop/archives")
        else:
            self.dirRow.set_subtitle(self.settings["periodic-saving-folder"])
        self.dirLBox.append(self.dirRow)
        self.dirDialog.set_extra_child(self.dirLBox)
        self.dirDialog.add_response('another-folder', _["set_another"])
        self.dirDialog.add_response('ok', _["apply"])
        self.dirDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.dirDialog.connect('response', self.dirdialog_closed)
        self.dirDialog.show()
        
    # Action after closed dialog for choosing periodic backups folder
    def dirdialog_closed(self, w, response):
        if response == 'another-folder':
            self.select_pb_folder()
        elif response == 'ok':
            if self.dirRow.get_subtitle() == '':
                self.settings["periodic-saving-folder"] = f'{download_dir}/SaveDesktop/archives'
            else:
                self.settings["periodic-saving-folder"] = self.dirRow.get_subtitle()
    
    # Select folder for periodic backups (Gtk.FileDialog)
    def select_pb_folder(self):
        def save_selected(source, res, data):
            try:
                file = source.select_folder_finish(res)
            except:
                return
            self.folder_pb = file.get_path()
            self.dirdialog()
            self.dirRow.set_subtitle(self.folder_pb)
        
        self.pb_chooser = Gtk.FileDialog.new()
        self.pb_chooser.set_modal(True)
        self.pb_chooser.set_title(_["set_pb_folder_tooltip"])
        self.pb_chooser.select_folder(self, None, save_selected, None)
    
    # Select folder for saving configuration
    def select_folder(self, w):
        def save_selected(source, res, data):
            try:
                file = source.select_folder_finish(res)
            except:
                return
            self.please_wait_toast()
            self.folder = file.get_path()
            self.save_config()
        
        if " " in self.saveEntry.get_text():
            self.with_spaces_text = self.saveEntry.get_text()
            self.filename_text = self.with_spaces_text.replace(" ", "_")
        else:
            self.filename_text = f'{self.saveEntry.get_text()}'
        
        self.folderchooser = Gtk.FileDialog.new()
        self.folderchooser.set_modal(True)
        self.folderchooser.set_title(_["save_config"])
        self.folderchooser.select_folder(self, None, save_selected, None)
            
    # Load file chooser
    def select_import_folder(self, w):
        def open_selected(source, res, data):
            try:
                file = source.open_finish(res)
            except:
                return
            self.please_wait_toast()
            if not os.path.exists(f'{CACHE}/import_config'):
                os.mkdir(f'{CACHE}/import_config')
            os.chdir(f'{CACHE}/import_config')
            os.system("tar -xf %s ./" % file.get_path())
            self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
        
        self.file_chooser = Gtk.FileDialog.new()
        self.file_chooser.set_modal(True)
        self.file_chooser.set_title(_["import_fileshooser"].format(self.environment))
        self.file_filter = Gtk.FileFilter.new()
        self.file_filter.set_name(_["savedesktop_f"])
        self.file_filter.add_pattern('*.sd.tar.gz')
        self.file_filter_list = Gio.ListStore.new(Gtk.FileFilter);
        self.file_filter_list.append(self.file_filter)
        self.file_chooser.set_filters(self.file_filter_list)
        self.file_chooser.open(self, None, open_selected, None)
    
    # Save configuration
    def save_config(self):
        # Create and load directory for saving configuration in CACHE
        if not os.path.exists(f"{CACHE}/saved_config"):
            os.mkdir(f"{CACHE}/saved_config")
        os.chdir(f"{CACHE}/saved_config")
        self.dconf = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/dconf/user ./")
        self.backgrounds = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/backgrounds ./")
        self.themes = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.themes ./")
        self.icons_home = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.icons ./")
        self.icons = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.local/share/icons ./")
        self.fonts = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.fonts ./")
        self.gtk4 = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/gtk-4.0 ./")
        self.gtk3 = GLib.spawn_command_line_async(f"cp -R {Path.home()}/.config/gtk-3.0 ./")
        if self.switch_01.get_active() == True:
            os.popen(f"sh {system_dir}/backup_flatpaks.sh")
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
        self.create_archive()
           
    # Create tarball archive
    def create_archive(self):
        # Get self.saveEntry text
        if self.saveEntry.get_text() == "":
            #self.create_classic_tar = GLib.spawn_command_line_async(f"tar --gzip -cf config_{date.today()}.sd.tar.gz ./")
            os.popen(f"tar --gzip -cf config_{date.today()}.sd.tar.gz ./")
            filename = f'config_{date.today()}'
        else:
            #self.create_classic_tar = GLib.spawn_command_line_async(f"tar --gzip -cf {self.saveEntry.get_text()}.sd.tar.gz ./")
            os.popen(f"tar --gzip -cf {self.filename_text}.sd.tar.gz ./")
            filename = f'{self.filename_text}'
        with open(f"{CACHE}/.filedialog.json", "w") as fd:
                fd.write('{\n "recent_file": "%s/%s.sd.tar.gz"\n}' % (self.folder, filename))
        self.tar_time = GLib.timeout_add_seconds(6, self.exporting_done)
        
    # Import config from list
    def imp_cfg_from_list(self, w):
        selected_archive = self.radio_row.get_selected_item()
        self.please_wait_toast()
        os.chdir("%s" % CACHE)
        os.popen("tar -xf %s/%s ./" % (self.dir, selected_archive.get_string()))
        self.tar_time = GLib.timeout_add_seconds(3, self.import_config)
            
    # Import configuration
    def import_config(self):
        # Applying configuration for GNOME-based environments
        if not os.path.exists("{}/.config".format(Path.home())):
            os.system("mkdir ~/.config/")
        # Create Dconf directory
        if not os.path.exists("{}/.config/dconf".format(Path.home())):
            os.system("mkdir ~/.config/dconf/")
        else:
            os.system('rm -rf ~/.config/dconf && mkdir ~/.config/dconf')
        self.i_dconf = GLib.spawn_command_line_async(f"cp ./user {Path.home()}/.config/dconf/")
        self.i_icons = GLib.spawn_command_line_async(f'cp -R ./icons {Path.home()}/.local/share/')
        self.i_themes = GLib.spawn_command_line_async(f'cp -R ./.themes {Path.home()}/')
        self.i_icons_home = GLib.spawn_command_line_async(f'cp -R ./.icons {Path.home()}/')
        self.i_backgrounds = GLib.spawn_command_line_async(f'cp -R ./backgrounds {Path.home()}/.local/share/')
        self.i_fonts = GLib.spawn_command_line_async(f'cp -R ./.fonts {Path.home()}/')
        self.i_gtk4 = GLib.spawn_command_line_async(f'cp -R ./gtk-4.0 {Path.home()}/.config/')
        self.i_gtk3 = GLib.spawn_command_line_async(f'cp -R ./gtk-3.0 {Path.home()}/.config/')
        self.flatpak_apps = GLib.spawn_command_line_async(f'cp ./installed_flatpaks.sh {DATA}/')
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
            os.chdir("%s/import_config" % CACHE)
            os.chdir('xdg-config')
            self.i_kconf = GLib.spawn_command_line_async(f'cp -R ./ {Path.home()}/.config/')
            os.chdir("%s/import_config" % CACHE)
            os.chdir('xdg-data')
            self.i_kdata = GLib.spawn_command_line_async(f'cp -R ./ {Path.home()}/.local/share/')
        self.create_flatpak_desktop()
        self.applying_done()
    
    # Create desktop for install Flatpaks from list
    def create_flatpak_desktop(self):
        os.popen(f"cp {system_dir}/install_flatpak_from_script.py {DATA}/")
        if not os.path.exists(f"{Path.home()}/.config/autostart"):
            os.mkdir(f"{Path.home()}/.config/autostart")
        if not os.path.exists(f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"):
            with open(f"{Path.home()}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop", "w") as fa:
                fa.write(f"[Desktop Entry]\nName=SaveDesktop (Flatpak Apps installer)\nType=Application\nExec=python3 {DATA}/install_flatpak_from_script.py")
    
    # configuration has been exported action
    def exporting_done(self):
        os.chdir(f"{CACHE}/saved_config")
        os.system(f"mv *.tar.gz {self.folder}/")
        self.toast.set_title(title=_["config_saved"])
        self.toast.set_button_label(_["open_folder"])
        self.toast.set_action_name("app.open_dir")
        self.toast_overlay.add_toast(self.toast)
    
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
    
    # Action after disappearancing toast
    def on_toast_dismissed(self, toast):
        os.popen("rm -rf %s/*" % CACHE)
    
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
        (width, height) = self.get_default_size()
        self.settings["window-size"] = (width, height)
        self.settings["maximized"] = self.is_maximized()
        self.settings["filename"] = self.saveEntry.get_text()
        self.settings["save-installed-flatpaks"] = self.switch_01.get_active()
        self.settings["periodic-saving"] = backup_item
        
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('about', self.on_about_action, ["F1"])
        self.create_action('open_dir', self.open_dir)
        self.create_action('logout', self.logout)
        self.connect('activate', self.on_activate)
        
    # Open directory (action after clicking button Open the folder on Adw.Toast)
    def open_dir(self, action, param):
        with open(f"{CACHE}/.filedialog.json") as fd:
            jf = json.load(fd)
        os.popen(f'dbus-send --session --print-reply --dest=org.freedesktop.FileManager1 --type=method_call /org/freedesktop/FileManager1 org.freedesktop.FileManager1.ShowItems array:string:"file://{jf["recent_file"]}" string:""')
        
    # Logout (action after clicking button Log Out on Adw.Toast)
    def logout(self, action, param):
        os.system("rm %s/*" % CACHE)
        if os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
            os.system("dbus-send --session --type=method_call --print-reply --dest=org.xfce.SessionManager /org/xfce/SessionManager org.xfce.Session.Manager.Logout boolean:true boolean:false")
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
            os.system("dbus-send --print-reply --dest=org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout int32:0 int32:0 int32:0")
        else:
            os.system("dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1")
        
    # About dialog
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("SaveDesktop")
        dialog.set_developer_name("vikdevelop")
        if r_lang == "en":
            print("")
        else:
            dialog.set_translator_credits(_["translator_credits"])
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/SaveDesktop")
        dialog.set_issue_url("https://github.com/vikdevelop/SaveDesktop/issues")
        dialog.set_copyright("© 2023 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_artists(["Brage Fuglseth"])
        version = "2.7.2"
        icon = "io.github.vikdevelop.SaveDesktop"
        if flatpak:
            if os.path.exists("/app/share/build-beta.sh"):
                dialog.set_version(f"{version}-beta")
                dialog.set_application_icon(f"{icon}.Devel")
            else:
                dialog.set_version(version)
                dialog.set_application_icon(icon)
        else:
            dialog.set_version(f"{version}-native")
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
