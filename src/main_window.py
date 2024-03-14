#!/usr/bin/python3
import os
import socket
import gi
import glob
import sys
import dbus
import shutil
from localization import _, home
from urllib.request import urlopen
from open_wiki import *
from shortcuts_window import *
from datetime import date
from pathlib import Path
from threading import Thread
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib

# Get user download dir
download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
if snap:
    os.makedirs(f"{CACHE}", exist_ok=True)

# Shortcuts window
@Gtk.Template(string=SHORTCUTS_WINDOW) # from shortcuts_window.py
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Application window
class MainWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("SaveDesktop")
        self.headerbar = Adw.HeaderBar.new()
        self.set_titlebar(titlebar=self.headerbar)
        self.application = kwargs.get('application')

        # Load the GSettings database for saving user settings
        self.settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
        
        self.different_toast_msg = False # value that sets if popup should be with text "Please wait ..." or "It'll take a few minutes ..."
        self.save_ext_switch_state = False # value that sets if state of the switch "Extensions" in the Items Dialog should be saved or not

        # Set the window size and maximization from the GSettings database
        self.set_size_request(750, 540)
        (width, height) = self.settings["window-size"]
        self.set_default_size(width, height)
        
        if self.settings["maximized"]:
            self.maximize()
        
        # App menu
        self.main_menu = Gio.Menu()
        self.general_menu = Gio.Menu()
        self.general_menu.append(_["about_app"], 'app.about')
        self.general_menu.append(_["keyboard_shortcuts"], 'app.shortcuts')
        self.main_menu.append_section(None, self.general_menu)
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.main_menu)
        self.headerbar.pack_end(child=self.menu_button)
        
        # Add Manually sync button
        if self.settings["manually-sync"] == True:
            self.sync_menu = Gio.Menu()
            self.sync_menu.append(_["sync"], 'app.m_sync')
            self.main_menu.append_section(None, self.sync_menu)
        
        # Primary layout
        self.headapp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.headapp.set_margin_start(80)
        self.headapp.set_margin_end(80)
        self.headapp.set_valign(Gtk.Align.CENTER)
        self.headapp.set_halign(Gtk.Align.CENTER)
        
        # Layout for import from list section
        self.pBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.pBox.set_halign(Gtk.Align.CENTER)
        self.pBox.set_valign(Gtk.Align.CENTER)
        
        # A view container for the menu switcher
        self.stack = Adw.ViewStack(vexpand=True)
        self.stack.set_hhomogeneous(True)
        self.headapp.append(self.stack)
        
        # Layout for saving and importing configuration
        self.saveBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=17)
        self.importBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.imp_cfg_title = _["import_from_file"]
        self.syncingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Add pages to the menu switcher
        self.stack.add_titled_with_icon(self.saveBox,"savepage",_["save"],"document-save-symbolic")
        self.stack.add_titled_with_icon(self.importBox,"importpage",_["import_title"],"document-open-symbolic")
        self.stack.add_titled_with_icon(self.syncingBox,"syncpage",_["sync"],"emblem-synchronizing-symbolic")
        
        # menu Switcher
        self.switcher_title=Adw.ViewSwitcherTitle()
        self.switcher_title.set_stack(self.stack)
        self.switcher_title.set_title("")
        self.headerbar.set_title_widget(self.switcher_title)
        
        # Toast Overlay for showing the popup window
        self.toast_overlay = Adw.ToastOverlay.new()
        self.toast_overlay.set_margin_top(margin=1)
        self.toast_overlay.set_margin_end(margin=1)
        self.toast_overlay.set_margin_bottom(margin=1)
        self.toast_overlay.set_margin_start(margin=1)
        
        # Set Toast Overlay as a application child
        self.set_child(self.toast_overlay)
        self.toast_overlay.set_child(self.headapp)

        # Popup window for showing messages about saved and imported configuration
        self.toast = Adw.Toast.new(title='')
        self.toast.set_timeout(0)
        
        # Check of user current desktop
        if os.getenv('XDG_CURRENT_DESKTOP') == 'GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'zorin:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'ubuntu:GNOME':
            self.environment = 'GNOME'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'pop:GNOME':
            self.environment = 'COSMIC'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Pantheon':
            self.environment = 'Pantheon'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'X-Cinnamon':
            self.environment = 'Cinnamon'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'Budgie:GNOME':
            self.environment = 'Budgie'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
            self.environment = 'Xfce'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'MATE':
            self.environment = 'MATE'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
            self.environment = 'KDE Plasma'
            self.save_desktop()
            self.import_desktop()
            self.syncing_desktop()
            self.connect("close-request", self.on_close)
        else:
            # If the user uses another desktop environment
            self.set_child(self.pBox)
            self.pBox.set_margin_start(50)
            self.pBox.set_margin_end(50)
            self.headerbar.set_title_widget(None)
            self.Image = Gtk.Image.new_from_icon_name("exclamation_mark")
            self.Image.set_pixel_size(50)
            self.pBox.append(self.Image)
            self.label_sorry = Gtk.Label()
            self.label_sorry.set_markup(_["unsuppurted_env_desc"].format("GNOME, Xfce, Budgie, Cinnamon, COSMIC, Pantheon, KDE Plasma, MATE"))
            self.label_sorry.set_wrap(True)
            self.label_sorry.set_justify(Gtk.Justification.CENTER)
            self.pBox.append(self.label_sorry)
            
        if snap:
            plugs = ["dot-config", "dot-local", "dot-themes", "dot-icons", "dot-fonts", "login-session-control"]            

            for plug in plugs:
                result = subprocess.run(["snapctl", "is-connected", plug], stdout=subprocess.PIPE)
                # If plug is not connected, display error message
                if result.returncode != 0:
                    show_warning = True
                else:
                    show_warning = False

            if show_warning == True:
                self.set_child(self.pBox)
                self.headerbar.set_title_widget(None)
                self.pBox.set_margin_start(90)
                self.pBox.set_margin_end(90)
                
                # show exclamation mark icon
                self.snapImage = Gtk.Image.new_from_icon_name("exclamation_mark")
                self.snapImage.set_pixel_size(50)
                self.pBox.append(self.snapImage)
                
                # show warning label
                self.snapLabel = Gtk.Label.new(str="<big><b>Need to connect some plugs</b></big>\nIn order for SaveDesktop to work properly, you need to connect some plugs to access the files. You can do this by opening a terminal (Ctrl+Alt+T) and entering the following command: \n")
                self.snapLabel.set_use_markup(True)
                self.snapLabel.set_justify(Gtk.Justification.CENTER)
                self.snapLabel.set_wrap(True)
                self.pBox.append(self.snapLabel)
                
                # show command text
                self.cmdLabel = Gtk.Label.new(str="<i>sudo snap connect savedesktop:dot-config &amp;&amp; sudo snap connect savedesktop:dot-local &amp;&amp; sudo snap connect savedesktop:dot-themes &amp;&amp; sudo snap connect savedesktop:dot-icons &amp;&amp; sudo snap connect savedesktop:dot-fonts &amp;&amp; sudo snap connect savedesktop:login-session-control</i>")
                self.cmdLabel.set_use_markup(True)
                self.cmdLabel.set_selectable(True)
                self.cmdLabel.set_justify(Gtk.Justification.CENTER)
                self.cmdLabel.set_wrap(True)
                self.pBox.append(self.cmdLabel)

                os.system(f"echo > {DATA}/first-run")
    
    # Show main layout
    def save_desktop(self):
        # Set margin for save desktop layout
        self.saveBox.set_margin_start(40)
        self.saveBox.set_margin_end(40)
        self.saveBox.set_valign(Gtk.Align.CENTER)
        
        # Title image for save page
        self.titleImage = Gtk.Image.new_from_icon_name("desktop-symbolic")
        self.titleImage.set_pixel_size(64)
        self.saveBox.append(self.titleImage)
        
        # Title "Save Current configuration" for save page and subtitle "{user_desktop}"
        self.label_title = Gtk.Label.new()
        self.label_title.set_markup('<big><b>{}</b></big>\n{}'.format(_["save_config"], self.environment))
        self.label_title.set_justify(Gtk.Justification.CENTER)
        self.saveBox.append(self.label_title)
        
        # Box for show this options: set the filename, set items that will be included to the config archive and periodic saving
        self.lbox_e = Gtk.ListBox.new()
        self.lbox_e.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.lbox_e.add_css_class(css_class='boxed-list')
        self.lbox_e.set_margin_start(27)
        self.lbox_e.set_margin_end(27)
        self.saveBox.append(self.lbox_e)
        
        # set the filename section
        self.saveEntry = Adw.EntryRow.new()
        self.saveEntry.set_title(_["set_filename"])
        self.saveEntry.set_text(self.settings["filename"])
        self.lbox_e.append(self.saveEntry)

        # Button for opening dialog for selecting items that will be included to the config archive
        self.itemsButton = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self.itemsButton.set_valign(Gtk.Align.CENTER)
        self.itemsButton.add_css_class("flat")
        self.itemsButton.connect("clicked", self.open_itemsDialog)

        # Action row for opening dialog for selecting items that will be included to the config archive
        self.items_row = Adw.ActionRow.new()
        self.items_row.set_title(title=_["items_for_archive"])
        self.items_row.set_use_markup(True)
        self.items_row.set_title_lines(3)
        self.items_row.set_subtitle_lines(3)
        self.items_row.add_suffix(self.itemsButton)
        self.items_row.set_activatable_widget(self.itemsButton)
        self.lbox_e.append(child=self.items_row)
        
        self.lbox_e.set_show_separators(True)
        
        # Periodic saving section
        actions = Gtk.StringList.new(strings=[
            _["never"], _["daily"], _["weekly"], _["monthly"]
        ])
        
        self.periodicButton = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self.periodicButton.add_css_class("flat")
        self.periodicButton.set_tooltip_text(_["more_settings_pb"])
        self.periodicButton.set_valign(Gtk.Align.CENTER)
        self.periodicButton.connect("clicked", self.open_periodic_backups)
        
        self.adw_action_row_backups = Adw.ComboRow.new()
        self.adw_action_row_backups.add_suffix(self.periodicButton)
        self.adw_action_row_backups.set_use_markup(True)
        self.adw_action_row_backups.set_use_underline(True)
        self.adw_action_row_backups.set_title(_["periodic_saving"])
        self.adw_action_row_backups.set_subtitle(f"{_['periodic_saving_desc']}\n<a href='{pb_wiki}'>{_['learn_more']}</a>")
        self.adw_action_row_backups.set_title_lines(2)
        self.adw_action_row_backups.set_subtitle_lines(4)
        self.adw_action_row_backups.set_model(model=actions)
        self.lbox_e.append(child=self.adw_action_row_backups)

        # Load options from GSettings database
        if self.settings["periodic-saving"] == 'Never':
            self.adw_action_row_backups.set_selected(0)
        elif self.settings["periodic-saving"] == 'Daily':
            self.adw_action_row_backups.set_selected(1)
        elif self.settings["periodic-saving"] == 'Weekly':
            self.adw_action_row_backups.set_selected(2)
        elif self.settings["periodic-saving"] == 'Monthly':
            self.adw_action_row_backups.set_selected(3)
        
        # Save configuration button
        self.saveButton = Gtk.Button.new_with_label(_["save"])
        self.saveButton.add_css_class("suggested-action")
        self.saveButton.add_css_class("pill")
        self.saveButton.connect("clicked", self.select_folder)
        self.saveButton.set_valign(Gtk.Align.CENTER)
        self.saveButton.set_halign(Gtk.Align.CENTER)
        self.saveBox.append(self.saveButton)
        
    # Import configuration section
    def import_desktop(self):
        self.importBox.set_valign(Gtk.Align.CENTER)
        self.importBox.set_halign(Gtk.Align.CENTER)
        
        # Image and title for Import page
        self.statusPage_i = Adw.StatusPage.new()
        self.statusPage_i.set_icon_name("document-open-symbolic")
        self.statusPage_i.set_title(_['import_config'])
        self.statusPage_i.set_description(_["import_config_desc"])
        self.statusPage_i.set_child(self.syncingBox)
        self.importBox.append(self.statusPage_i)
        
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
                
    # Import archive from list
    def import_from_list(self, w):
        self.toast_overlay.set_child(self.pBox)
        self.backButton = Gtk.Button.new_from_icon_name("go-next-symbolic-rtl")
        self.backButton.add_css_class("flat")
        self.backButton.connect("clicked", self.close_list)
        self.headerbar.set_title_widget(None)
        self.set_title(_["import_from_list"])
        self.headerbar.pack_start(self.backButton)

        # Box for this section
        self.flistBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.pBox.append(self.flistBox)

        # Label for showing text in this section
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

                # Button for applying selected archive
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

                # Get SaveDesktop files from folder selected by the user
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
            
    # Syncing desktop page
    def syncing_desktop(self):
        self.syncingBox.set_valign(Gtk.Align.CENTER)
        self.syncingBox.set_halign(Gtk.Align.CENTER)
        self.syncingBox.set_margin_start(40)
        self.syncingBox.set_margin_end(40)

        # Replace the old URL about syncing in the translation string with a new URL
        if "https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network" in _["sync_desc"]:
            old_url = _["sync_desc"]
            new_url = old_url.replace("https://github.com/vikdevelop/SaveDesktop/wiki/Synchronization-between-computers-in-the-network", f'{sync_wiki}')
        else:
            new_url = _["sync_desc"]

        # Image and title for this page
        self.statusPage = Adw.StatusPage.new()
        self.statusPage.set_icon_name("emblem-synchronizing-symbolic")
        self.statusPage.set_title(_["sync_title"])
        self.statusPage.set_description(new_url)
        self.statusPage.set_child(self.syncingBox)
        self.syncingBox.append(self.statusPage)

        # "Set up the sync file" button
        self.setButton = Gtk.Button.new_with_label(_["set_up_sync_file"])
        self.setButton.add_css_class("pill")
        self.setButton.add_css_class("suggested-action")
        self.setButton.connect("clicked", self.setButton_dialog)
        self.setButton.set_valign(Gtk.Align.CENTER)
        self.setButton.set_margin_start(70)
        self.setButton.set_margin_end(70)
        self.syncingBox.append(self.setButton)

        # "Connect with other computer" button
        self.getButton = Gtk.Button.new_with_label(_["connect_with_other_computer"])
        self.getButton.add_css_class("pill")
        self.getButton.connect("clicked", self.open_urlDialog)
        self.getButton.set_valign(Gtk.Align.CENTER)
        self.getButton.set_margin_start(70)
        self.getButton.set_margin_end(70)
        self.syncingBox.append(self.getButton)
        
    # Open set Dialog by clicking on "Set up the sync file" button
    def setButton_dialog(self, w):
        self.open_setDialog()

    # Dialog for setting the sync file, periodic synchronization interval and copying the URL for synchronization
    def open_setDialog(self):
        self.setDialog = Adw.MessageDialog.new(self)
        self.setDialog.set_heading(_["set_up_sync_file"])
        self.setDialog.set_body_use_markup(True)

        # Box for appending widgets
        self.setdBox = Gtk.ListBox.new()
        self.setdBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.setdBox.get_style_context().add_class(class_name='boxed-list')
        self.setDialog.set_extra_child(self.setdBox)

        # Button for choosing synchronization file
        self.selsetButton = Gtk.Button.new_from_icon_name("document-open-symbolic")
        self.selsetButton.set_valign(Gtk.Align.CENTER)
        self.selsetButton.connect("clicked", self.select_syncfile)

        # Row for showing selected synchronization file
        self.file_row = Adw.ActionRow.new()
        self.file_row.set_title("1 " + _["periodic_saving_file"])
        self.file_row.set_subtitle(self.settings["file-for-syncing"])
        self.file_row.add_suffix(self.selsetButton)
        self.setdBox.append(self.file_row)
        
        # Periodic sync section
        actions = Gtk.StringList.new(strings=[
            _["never"], _["daily"], _["weekly"], _["monthly"], _["manually"]
        ])
        
        self.import_row = Adw.ComboRow.new()
        self.import_row.add_suffix(self.periodicButton)
        self.import_row.set_use_markup(True)
        self.import_row.set_use_underline(True)
        self.import_row.set_title("2 " + _["periodic_sync"])
        self.import_row.set_title_lines(2)
        self.import_row.set_subtitle_lines(4)
        self.import_row.set_model(model=actions)
        self.setdBox.append(child=self.import_row)

        # Load periodic sync values form GSettings database
        if self.settings["periodic-import"] == "Never2":
            self.import_row.set_selected(0)
        elif self.settings["periodic-import"] == "Daily2":
            self.import_row.set_selected(1)
        elif self.settings["periodic-import"] == "Weekly2":
            self.import_row.set_selected(2)
        elif self.settings["periodic-import"] == "Monthly2":
            self.import_row.set_selected(3)
        elif self.settings["periodic-import"] == "Manually2":
            self.import_row.set_selected(4)

        # Action row for showing URL for synchronization with other computers
        self.url_row = Adw.ActionRow.new()
        self.url_row.set_title("3 " + _["url_for_sync"])
        self.url_row.set_use_markup(True)
        self.url_row.set_subtitle(f"http://{IPAddr}:8000")
        self.url_row.set_subtitle_selectable(True)
        self.setdBox.append(self.url_row)
        
        self.setDialog.add_response('cancel', _["cancel"])
        self.setDialog.add_response('ok', _["apply"])
        self.setDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.setDialog.connect('response', self.setDialog_closed)
        
        self.setDialog.show()

    # Action after closing dialog for setting synchronization file
    def setDialog_closed(self, w, response):
        if response == 'ok':
            self.set_syncing()
            
            # Check periodic synchronization variable BEFORE saving to GSettings database
            with open(f"{CACHE}/.sync", "w") as s:
                s.write(f"{self.settings['periodic-import']}")
            
            # Save the sync file to the GSettings database
            self.file_name = os.path.basename(self.file_row.get_subtitle())
            self.file = os.path.splitext(self.file_name)[0]
            self.path = Path(self.file_row.get_subtitle())
            self.folder = self.path.parent.absolute()
            
            self.settings["file-for-syncing"] = self.file_row.get_subtitle()

            # Set filename format to same as the sync file name
            r_file = self.file.replace(".sd.tar", "")
            self.settings["filename-format"] = r_file
            
            # Set periodic saving folder to same as the folder for the sync file
            self.settings["periodic-saving-folder"] = f'{self.folder}'

            # Save periodic synchronization interval to remote file and the GSettings database
            selected_item = self.import_row.get_selected_item()
            if selected_item.get_string() == _["never"]:
                import_item = "Never2"
            elif selected_item.get_string() == _["daily"]:
                import_item = "Daily2"
            elif selected_item.get_string() == _["weekly"]:
                import_item = "Weekly2"
            elif selected_item.get_string() == _["monthly"]:
                import_item = "Monthly2"
            elif selected_item.get_string() == _["manually"]:
                import_item = "Manually2"
            if not os.path.exists(f"{DATA}/synchronization"):
                os.mkdir(f"{DATA}/synchronization")
            with open(f"{DATA}/synchronization/file-settings.json", "w") as f:
                f.write('{\n "file-name": "%s.gz",\n "periodic-import": "%s"\n}' % (self.file, import_item))
            self.settings["periodic-import"] = import_item
            sync_before = subprocess.getoutput(f"cat {CACHE}/.sync")
            if sync_before == "Never2":
                if not self.settings["periodic-import"] == "Never2":
                    self.show_warn_toast()

    # URL Dialog
    def open_urlDialog(self, w):
        self.urlDialog = Adw.MessageDialog.new(self)
        self.urlDialog.set_heading(_["connect_with_other_computer"])
        self.urlDialog.set_body(_["connect_with_pc_desc"])

        # Box for adding widgets in this dialog
        self.urlBox = Gtk.ListBox.new()
        self.urlBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.urlBox.get_style_context().add_class(class_name='boxed-list')
        self.urlDialog.set_extra_child(self.urlBox)

        # Entry for entering the URL for synchronization
        self.urlEntry = Adw.EntryRow.new()
        self.urlEntry.set_title(_["pc_url_entry"])
        self.urlEntry.set_text(self.settings["url-for-syncing"])
        self.urlBox.append(self.urlEntry)
        
        self.urlDialog.add_response('cancel', _["cancel"])
        self.urlDialog.add_response('ok', _["apply"])
        self.urlDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.urlDialog.connect('response', self.urlDialog_closed)
        self.urlDialog.show()

    # Action after closing URL dialog
    def urlDialog_closed(self, w, response):
        if response == 'ok':
            self.settings["url-for-syncing"] = self.urlEntry.get_text()
            self.folder = self.settings["file-for-syncing"]
            if not self.urlEntry.get_text() == "":
                r_file = urlopen(f"{self.settings['url-for-syncing']}/file-settings.json")
                jS = json.load(r_file)
                # Check if periodic synchronization interval is Manually option => if YES, add Sync button to the menu in the headerbar
                if jS["periodic-import"] == "Manually2":
                    self.settings["manually-sync"] = True
                    self.sync_menu = Gio.Menu()
                    self.sync_menu.append(_["sync"], 'app.m_sync')
                    self.main_menu.append_section(None, self.sync_menu)
                    self.set_syncing()
                    self.show_special_toast()
                    self.sync_menu.remove(1)
                else:
                    self.set_syncing()
                    self.show_warn_toast()
                    self.settings["manually-sync"] = False
                    self.sync_menu.remove(0)
            else:
                self.settings["manually-sync"] = False
                self.sync_menu.remove(0)

    # Set synchronization for running in the background
    def set_syncing(self):
        if not os.path.exists(f"{home}/.config/autostart"):
            os.mkdir(f"{home}/.config/autostart")
        # Create desktop file for running Python HTTP server
        if not os.path.exists(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.server.desktop"):
            with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.server.desktop", "w") as sv:
                sv.write(f'[Desktop Entry]\nName=SaveDesktop (syncing server)\nType=Application\nExec={server_cmd}')
        # Create desktop file for syncing the configuration from other computer
        if not os.path.exists(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.sync.desktop"):
            with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.sync.desktop", "w") as pv:
                pv.write(f'[Desktop Entry]\nName=SaveDesktop (syncing tool)\nType=Application\nExec={sync_cmd}')
            #self.show_warn_toast()
    
    # Set custom folder for periodic saving dialog
    def open_periodic_backups(self, w):
        self.dirdialog()
        
    # Dialog for changing directory for periodic backups
    def dirdialog(self):
        self.dirDialog = Adw.MessageDialog.new(app.get_active_window())
        # Gtk box for adding the label and list box widget
        self.dirBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # Title
        self.pbLabel = Gtk.Label.new(str=f"<big><b>{_['more_settings_pb']}</b></big>\n")
        self.pbLabel.set_use_markup(True)
        self.pbLabel.set_wrap(True)
        self.pbLabel.set_justify(Gtk.Justification.CENTER)
        self.dirBox.append(self.pbLabel)
        
        # Box for adding widgets in this dialog
        self.dirLBox = Gtk.ListBox.new()
        self.dirLBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.dirLBox.get_style_context().add_class(class_name='boxed-list')
        self.dirBox.append(self.dirLBox)

        # Restore filename format text to default
        self.filefrmtButton = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        self.filefrmtButton.add_css_class('destructive-action')
        self.filefrmtButton.set_valign(Gtk.Align.CENTER)
        self.filefrmtButton.set_tooltip_text(_["reset_button"])
        self.filefrmtButton.connect("clicked", self.set_default_filefrmtEntry)

        # Button for opening more information (on Wiki)
        self.helpButton = Gtk.Button.new_from_icon_name("help-about-symbolic")
        self.helpButton.add_css_class("flat")
        self.helpButton.set_valign(Gtk.Align.CENTER)
        self.helpButton.set_tooltip_text(_["learn_more"])
        self.helpButton.connect("clicked", self.open_fileformat_link)
        
        # Entry for selecting file name format
        self.filefrmtEntry = Adw.EntryRow.new()
        self.filefrmtEntry.set_title(_["filename_format"])
        self.filefrmtEntry.add_suffix(self.filefrmtButton)
        self.filefrmtEntry.add_suffix(self.helpButton)
        self.filefrmtEntry.set_text(self.settings["filename-format"])
        self.dirLBox.append(self.filefrmtEntry)
        
        # Button for choosing folder for periodic saving
        self.folderButton = Gtk.Button.new_from_icon_name("document-open-symbolic")
        self.folderButton.set_valign(Gtk.Align.CENTER)
        self.folderButton.set_tooltip_text(_["set_another"])
        self.folderButton.connect("clicked", self.select_pb_folder)
        
        # Adw.ActionRow for showing folder for periodic saving
        self.dirRow = Adw.ActionRow.new()
        self.dirRow.set_title(_["pb_folder"])
        self.dirRow.add_suffix(self.folderButton)
        self.dirRow.set_use_markup(True)
        if self.settings["periodic-saving-folder"] == '':
            self.dirRow.set_subtitle(f"{download_dir}/SaveDesktop/archives")
        else:
            self.dirRow.set_subtitle(self.settings["periodic-saving-folder"])
        self.dirLBox.append(self.dirRow)
        
        self.dirDialog.set_extra_child(self.dirBox)
        self.dirDialog.add_response('cancel', _["cancel"])
        self.dirDialog.add_response('ok', _["apply"])
        self.dirDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.dirDialog.connect('response', self.dirdialog_closed)
        self.dirDialog.show()
        
    # Action after closed dialog for choosing periodic backups folder
    def dirdialog_closed(self, w, response):
        if response == 'ok':
            if self.dirRow.get_subtitle() == '':
                self.settings["periodic-saving-folder"] = f'{download_dir}/SaveDesktop/archives'
            else:
                self.settings["periodic-saving-folder"] = self.dirRow.get_subtitle()
            self.settings["filename-format"] = self.filefrmtEntry.get_text()
            
    # Set text of self.filefrmtEntry to default
    def set_default_filefrmtEntry(self, w):
        self.filefrmtEntry.set_text("Latest_configuration")

    # Open Wiki by clicking on the self.helpButton
    def open_fileformat_link(self, w):
        os.system(f"xdg-open {pb_wiki}#filename-format")
            
    # Dialog: items to include in the configuration archive
    def open_itemsDialog(self, w):
        self.itemsDialog = Adw.MessageDialog.new(app.get_active_window())
        self.itemsDialog.set_heading(_["items_for_archive"])
        self.itemsDialog.set_body(_["items_desc"])
        self.itemsDialog.set_default_size(400, 200)
        
        # Box for loading widgets in this dialog
        self.itemsBox = Gtk.ListBox.new()
        self.itemsBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.itemsBox.get_style_context().add_class(class_name='boxed-list')
        self.itemsDialog.set_extra_child(self.itemsBox)
        
        # Switch and row of option 'Save icons'
        self.switch_01 = Gtk.Switch.new()
        if self.settings["save-icons"]:
            self.switch_01.set_active(True)
        self.switch_01.set_valign(align=Gtk.Align.CENTER)
         
        self.icons_row = Adw.ActionRow.new()
        self.icons_row.set_title(title=_["icons"])
        self.icons_row.set_use_markup(True)
        self.icons_row.set_title_lines(2)
        self.icons_row.set_subtitle_lines(3)
        self.icons_row.add_suffix(self.switch_01)
        self.icons_row.set_activatable_widget(self.switch_01)
        self.itemsBox.append(child=self.icons_row)
        
        # Switch and row of option 'Save themes'
        self.switch_02 = Gtk.Switch.new()
        if self.settings["save-themes"]:
            self.switch_02.set_active(True)
        self.switch_02.set_valign(align=Gtk.Align.CENTER)
         
        self.themes_row = Adw.ActionRow.new()
        self.themes_row.set_title(title=_["themes"])
        self.themes_row.set_use_markup(True)
        self.themes_row.set_title_lines(2)
        self.themes_row.set_subtitle_lines(3)
        self.themes_row.add_suffix(self.switch_02)
        self.themes_row.set_activatable_widget(self.switch_02)
        self.itemsBox.append(child=self.themes_row)
        
        # Switch and row of option 'Save fonts'
        self.switch_03 = Gtk.Switch.new()
        if self.settings["save-fonts"]:
            self.switch_03.set_active(True)
        self.switch_03.set_valign(align=Gtk.Align.CENTER)
         
        self.fonts_row = Adw.ActionRow.new()
        self.fonts_row.set_title(title=_["fonts"])
        self.fonts_row.set_use_markup(True)
        self.fonts_row.set_title_lines(2)
        self.fonts_row.set_subtitle_lines(3)
        self.fonts_row.add_suffix(self.switch_03)
        self.fonts_row.set_activatable_widget(self.switch_03)
        self.itemsBox.append(child=self.fonts_row)
        
        # Switch and row of option 'Save backgrounds'
        self.switch_04 = Gtk.Switch.new()
        if self.settings["save-backgrounds"]:
            self.switch_04.set_active(True)
        self.switch_04.set_valign(align=Gtk.Align.CENTER)
         
        self.backgrounds_row = Adw.ActionRow.new()
        self.backgrounds_row.set_title(title=_["backgrounds"])
        self.backgrounds_row.set_use_markup(True)
        self.backgrounds_row.set_title_lines(2)
        self.backgrounds_row.set_subtitle_lines(3)
        self.backgrounds_row.add_suffix(self.switch_04)
        self.backgrounds_row.set_activatable_widget(self.switch_04)
        self.itemsBox.append(child=self.backgrounds_row)
        
        # Switch and row of option 'Save backgrounds'
        self.switch_de = Gtk.Switch.new()
        if self.settings["save-desktop-folder"]:
            self.switch_de.set_active(True)
        self.switch_de.set_valign(align=Gtk.Align.CENTER)
        
        if self.environment == "GNOME":
            self.save_ext_switch_state = True
            self.show_extensions_row()
        elif self.environment == "KDE Plasma":
            self.save_ext_switch_state = True
            self.show_extensions_row()
        elif self.environment == "Cinnamon":
            self.save_ext_switch_state = True
            self.show_extensions_row()
            
        self.desktop_row = Adw.ActionRow.new()
        self.desktop_row.set_title(title=_["desktop_folder"])
        self.desktop_row.set_subtitle(subtitle=GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP))
        self.desktop_row.set_subtitle_selectable(True)
        self.desktop_row.set_use_markup(True)
        self.desktop_row.set_title_lines(2)
        self.desktop_row.set_subtitle_lines(3)
        self.desktop_row.add_suffix(self.switch_de)
        self.desktop_row.set_activatable_widget(self.switch_de)
        self.itemsBox.append(child=self.desktop_row)
        
        if flatpak: 
            self.flatpak_row = Adw.ExpanderRow.new()
            self.flatpak_row.set_title(title=_["save_installed_flatpaks"])
            self.flatpak_row.set_subtitle(f'<a href="{flatpak_wiki}">{_["learn_more"]}</a>')
            self.flatpak_row.set_use_markup(True)
            self.flatpak_row.set_title_lines(2)
            self.flatpak_row.set_subtitle_lines(3)
            self.itemsBox.append(child=self.flatpak_row)
            
            # Switch and row of option 'Save installed flatpaks'
            self.switch_05 = Gtk.Switch.new()
            if self.settings["save-installed-flatpaks"]:
                self.switch_05.set_active(True)
            self.switch_05.set_valign(align=Gtk.Align.CENTER)
            
            self.list_row = Adw.ActionRow.new()
            self.list_row.set_title(title=_["list"])
            self.list_row.set_use_markup(True)
            self.list_row.set_title_lines(4)
            self.list_row.add_suffix(self.switch_05)
            self.list_row.set_activatable_widget(self.switch_05)
            self.flatpak_row.add_row(child=self.list_row)
            
            # Switch and row of option 'Save SaveDesktop app settings'
            self.switch_06 = Gtk.Switch.new()
            if self.settings["save-flatpak-data"]:
                self.switch_06.set_active(True)
            self.switch_06.set_valign(align=Gtk.Align.CENTER)
                
            self.data_row = Adw.ActionRow.new()
            self.data_row.set_title(title=_["user_data_flatpak"])
            self.data_row.set_use_markup(True)
            self.data_row.set_title_lines(4)
            self.data_row.add_suffix(self.switch_06)
            self.data_row.set_activatable_widget(self.switch_06)
            self.flatpak_row.add_row(child=self.data_row)
            
        self.itemsDialog.add_response('cancel', _["cancel"])
        self.itemsDialog.add_response('ok', _["apply"])
        self.itemsDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.itemsDialog.connect('response', self.itemsdialog_closed)
        self.itemsDialog.show()
        
    # Action after closing itemsDialog
    def itemsdialog_closed(self, w, response):
        if response == 'ok':
            # Saving the selected options to GSettings database
            self.settings["save-icons"] = self.switch_01.get_active()
            self.settings["save-themes"] = self.switch_02.get_active()
            self.settings["save-fonts"] = self.switch_03.get_active()
            self.settings["save-backgrounds"] = self.switch_04.get_active()
            self.settings["save-desktop-folder"] = self.switch_de.get_active()
            if flatpak:
                self.settings["save-installed-flatpaks"] = self.switch_05.get_active()
                self.settings["save-flatpak-data"] = self.switch_06.get_active()
            if self.save_ext_switch_state == True:
                self.settings["save-extensions"] = self.switch_ext.get_active()
            
    def show_extensions_row(self):
        # Switch and row of option 'Save extensions'
        self.switch_ext = Gtk.Switch.new()
        if self.settings["save-extensions"]:
            self.switch_ext.set_active(True)
        self.switch_ext.set_valign(align=Gtk.Align.CENTER)
         
        self.ext_row = Adw.ActionRow.new()
        self.ext_row.set_title(title=_["extensions"])
        self.ext_row.set_use_markup(True)
        self.ext_row.set_title_lines(2)
        self.ext_row.set_subtitle_lines(3)
        self.ext_row.add_suffix(self.switch_ext)
        self.ext_row.set_activatable_widget(self.switch_ext)
        self.itemsBox.append(child=self.ext_row)
    
    # Select folder for periodic backups (Gtk.FileDialog)
    def select_pb_folder(self, w):
        def save_selected(source, res, data):
            try:
                file = source.select_folder_finish(res)
            except:
                return
            self.folder_pb = file.get_path()
            self.dirdialog()
            self.dirRow.set_subtitle(self.folder_pb)
            
        self.dirDialog.close()
        
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
            self.folder = file.get_path()
            self.save_config()
        
        if self.saveEntry.get_text() == "":
            self.filename_text = "config"
        else:
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
            with open(f"{CACHE}/.impfile.json", "w") as j:
                j.write('{\n "import_file": "%s"\n}' % file.get_path())
            self.import_config()
        
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
        
    # Select file for syncing with other computers in the network
    def select_syncfile(self, w):
        def set_selected(source, res, data):
            try:
                file = source.open_finish(res)
            except:
                return
            self.syncfile = file.get_path()
            self.open_setDialog()
            self.file_row.set_subtitle(self.syncfile)
            if not os.path.exists(f"{DATA}/synchronization"):
                os.mkdir(f"{DATA}/synchronization")
            os.chdir(f"{DATA}/synchronization")
            os.popen(f"cp {self.syncfile} ./")
            
        self.setDialog.close()
        
        self.syncfile_chooser = Gtk.FileDialog.new()
        self.syncfile_chooser.set_modal(True)
        self.syncfile_chooser.set_title(_["set_up_sync_file"])
        self.file_filter_s = Gtk.FileFilter.new()
        self.file_filter_s.set_name(_["savedesktop_f"])
        self.file_filter_s.add_pattern('*.sd.tar.gz')
        self.file_filter_list_s = Gio.ListStore.new(Gtk.FileFilter);
        self.file_filter_list_s.append(self.file_filter_s)
        self.syncfile_chooser.set_filters(self.file_filter_list_s)
        self.syncfile_chooser.open(self, None, set_selected, None)
    
    # Save configuration
    def save_config(self):
        self.please_wait_save()
        with open(f"{CACHE}/.filedialog.json", "w") as w:
            w.write('{\n "recent_file": "%s/%s.sd.tar.gz"\n}' % (self.folder, self.filename_text))
        if not os.path.exists(f"{CACHE}/save_config"):
            os.mkdir(f"{CACHE}/save_config")
        os.chdir(f"{CACHE}/save_config")
        copy_thread = Thread(target=self.open_config_save)
        copy_thread.start()
        
    def open_config_save(self):
        try:
            os.system(f"python3 {system_dir}/config.py --save")
        except Exception as e:
            print("Can't run the config.py file!")
        finally:
            GLib.idle_add(self.exporting_done)
        
    # Import config from list
    def imp_cfg_from_list(self, w):
        selected_archive = self.radio_row.get_selected_item()
        if not os.path.exists(f"{CACHE}/import_from_list"):
            os.mkdir(f"{CACHE}/import_from_list")
        os.chdir(f"{CACHE}/import_from_list")
        with open(f"{CACHE}/.impfile.json", "w") as j:
            j.write('{\n "import_file": "%s/%s"\n}' % (self.dir, selected_archive.get_string()))
        self.import_config()
            
    # Import configuration
    def import_config(self):
        self.please_wait_import()
        if not os.path.exists(f"{CACHE}/import_config"):
            os.mkdir(f"{CACHE}/import_config")
        os.chdir(f"{CACHE}/import_config")
        copy_thread = Thread(target=self.open_config_import)
        copy_thread.start()
        
    def open_config_import(self):
        try:
            os.system(f"rm -rf {CACHE}/import_config/*")
            os.system(f"python3 {system_dir}/config.py --import_")
        except Exception as e:
            print("Can't run the config.py file!")
        finally:
            GLib.idle_add(self.applying_done)
            
    # "Please wait" information page on the "Save" page
    def please_wait_save(self):
        def cancel_save(w):
            os.system(f"pkill -xf 'python3 {system_dir}/config.py --save'")
            self.toast_overlay.set_child(self.headapp)
            self.savewaitBox.remove(self.savewaitSpinner)
            self.savewaitBox.remove(self.savewaitLabel)
            self.savewaitBox.remove(self.savewaitButton)
            self.savewaitBox.remove(self.sdoneImage)
            self.savewaitBox.remove(self.opensaveButton)
            self.savewaitBox.remove(self.backtomButton)
        
        self.savewaitBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.savewaitBox.set_halign(Gtk.Align.CENTER)
        self.savewaitBox.set_valign(Gtk.Align.CENTER)
        self.savewaitBox.set_margin_start(80)
        self.savewaitBox.set_margin_end(80)
        self.toast_overlay.set_child(self.savewaitBox)
        
        self.savewaitSpinner = Gtk.Spinner.new()
        self.savewaitSpinner.set_size_request(100,100)
        self.savewaitSpinner.start()
        self.savewaitBox.append(self.savewaitSpinner)
        
        self.sdoneImage = Gtk.Image.new()
        self.savewaitBox.append(self.sdoneImage)
        
        self.savewaitLabel = Gtk.Label.new(str="<big><b>Saving configuration ...</b></big>\nThe configuration of your desktop environment will be saved in:\n <i>{}/{}.sd.tar.gz</i>\n".format(self.folder, self.filename_text))
        self.savewaitLabel.set_use_markup(True)
        self.savewaitLabel.set_justify(Gtk.Justification.CENTER)
        self.savewaitLabel.set_wrap(True)
        self.savewaitBox.append(self.savewaitLabel)
        
        self.savewaitButton = Gtk.Button.new_with_label(_["cancel"])
        self.savewaitButton.add_css_class("pill")
        self.savewaitButton.add_css_class("destructive-action")
        self.savewaitButton.connect("clicked", cancel_save)
        self.savewaitButton.set_margin_start(170)
        self.savewaitButton.set_margin_end(170)
        self.savewaitBox.append(self.savewaitButton)
        
    # configuration has been exported action
    def exporting_done(self):
        def back_to_main(w):
            self.toast_overlay.set_child(self.headapp)
            self.savewaitBox.remove(self.savewaitSpinner)
            self.savewaitBox.remove(self.savewaitLabel)
            self.savewaitBox.remove(self.savewaitButton)
            self.savewaitBox.remove(self.sdoneImage)
            self.savewaitBox.remove(self.opensaveButton)
            self.savewaitBox.remove(self.backtomButton)
            
        if os.path.exists(f"{CACHE}/save_config/done_gui"):
            self.savewaitSpinner.stop()
            self.savewaitBox.remove(self.savewaitButton)
            # Done icon
            self.sdoneImage.set_from_icon_name("done")
            self.sdoneImage.set_pixel_size(128)
            
            self.savewaitLabel.set_label(f"<big><b>{_['config_saved']}</b></big>\nYou can now view the archive with the configuration of your desktop environment, or return to the previous page.\n")
            self.opensaveButton = Gtk.Button.new_with_label(_["open_folder"])
            self.opensaveButton.add_css_class('pill')
            self.opensaveButton.add_css_class('suggested-action')
            self.opensaveButton.set_action_name('app.open-dir')
            self.opensaveButton.set_margin_start(170)
            self.opensaveButton.set_margin_end(170)
            self.savewaitBox.append(self.opensaveButton)
            
            self.backtomButton = Gtk.Button.new_with_label("Back to previous page")
            self.backtomButton.connect("clicked", back_to_main)
            self.backtomButton.add_css_class("pill")
            self.backtomButton.set_margin_start(170)
            self.backtomButton.set_margin_end(170)
            self.savewaitBox.append(self.backtomButton)
            
        os.popen(f"rm -rf {CACHE}/save_config/*")
    
    # "Please wait" information on the "Import" page
    def please_wait_import(self):
        def cancel_import(w):
            os.system(f"pkill -xf 'python3 {system_dir}/config.py --import'")
            self.toast_overlay.set_child(self.headapp)
            self.importwaitBox.remove(self.importwaitSpinner)
            self.importwaitBox.remove(self.importwaitLabel)
            self.importwaitBox.remove(self.importwaitButton)
            self.importwaitBox.remove(self.idoneImage)
            self.importwaitBox.remove(self.logoutButton)
            self.importwaitBox.remove(self.backtomButton)
            
        with open(f'{CACHE}/.impfile.json') as i:
            ij = json.load(i)
        config_name = ij["import_file"]
        
        self.importwaitBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.importwaitBox.set_halign(Gtk.Align.CENTER)
        self.importwaitBox.set_valign(Gtk.Align.CENTER)
        self.importwaitBox.set_margin_start(80)
        self.importwaitBox.set_margin_end(80)
        self.toast_overlay.set_child(self.importwaitBox)
        
        self.importwaitSpinner = Gtk.Spinner.new()
        self.importwaitSpinner.set_size_request(100,100)
        self.importwaitSpinner.start()
        self.importwaitBox.append(self.importwaitSpinner)
        
        self.idoneImage = Gtk.Image.new()
        self.importwaitBox.append(self.idoneImage)
        
        self.importwaitLabel = Gtk.Label.new(str="<big><b>Importing configuration ...</b></big>\nImporting configuration from: {}\n".format(config_name))
        self.importwaitLabel.set_use_markup(True)
        self.importwaitLabel.set_justify(Gtk.Justification.CENTER)
        self.importwaitLabel.set_wrap(True)
        self.importwaitBox.append(self.importwaitLabel)
        
        self.importwaitButton = Gtk.Button.new_with_label(_["cancel"])
        self.importwaitButton.add_css_class("pill")
        self.importwaitButton.add_css_class("destructive-action")
        self.importwaitButton.connect("clicked", cancel_import)
        self.importwaitButton.set_margin_start(170)
        self.importwaitButton.set_margin_end(170)
        self.importwaitBox.append(self.importwaitButton)
        
    
    # Config has been imported action
    def applying_done(self):
        def back_to_main(w):
            self.toast_overlay.set_child(self.headapp)
            self.importwaitBox.remove(self.importwaitSpinner)
            self.importwaitBox.remove(self.importwaitLabel)
            self.importwaitBox.remove(self.importwaitButton)
            self.importwaitBox.remove(self.idoneImage)
            self.importwaitBox.remove(self.logoutButton)
            self.importwaitBox.remove(self.backtomButton)
            
        if os.path.exists(f"{CACHE}/import_config/done"):
            self.importwaitSpinner.stop()
            self.importwaitBox.remove(self.importwaitButton)
            
            # Done icon
            self.idoneImage.set_from_icon_name("done")
            self.idoneImage.set_pixel_size(128)
            
            self.importwaitLabel.set_label(f"<big><b>{_['config_imported']}</b></big>\nYou can log out of the system for the changes to take effect, or go back to the previous page and log out later.\n")
            self.logoutButton = Gtk.Button.new_with_label(_["logout"])
            self.logoutButton.add_css_class('pill')
            self.logoutButton.add_css_class('suggested-action')
            self.logoutButton.set_action_name('app.logout')
            self.logoutButton.set_margin_start(170)
            self.logoutButton.set_margin_end(170)
            self.importwaitBox.append(self.logoutButton)
            
            self.backtomButton = Gtk.Button.new_with_label("Back to previous page")
            self.backtomButton.connect("clicked", back_to_main)
            self.backtomButton.add_css_class("pill")
            self.backtomButton.set_margin_start(170)
            self.backtomButton.set_margin_end(170)
            self.importwaitBox.append(self.backtomButton)
       
    # a warning indicating that the user must log out
    def show_warn_toast(self):
        self.warn_toast = Adw.Toast.new(title=_["periodic_saving_desc"])
        self.warn_toast.set_button_label(_["logout"])
        self.warn_toast.set_action_name("app.logout")
        self.toast_overlay.add_toast(self.warn_toast)
        
    # message that says where will be run a synchronization
    def show_special_toast(self):
        self.special_toast = Adw.Toast.new(title=_["m_sync_desc"])
        self.toast_overlay.add_toast(self.special_toast)
    
    # action after closing window
    def on_close(self, widget, *args):
        self.close()
        selected_item = self.adw_action_row_backups.get_selected_item()
        # Translate backup items to English because it is necessary for the proper functioning of periodic backups correctly
        if selected_item.get_string() == _["never"]:
            backup_item = "Never"
        elif selected_item.get_string() == _["daily"]:
            backup_item = "Daily"
            self.create_pb_desktop()
        elif selected_item.get_string() == _["weekly"]:
            backup_item = "Weekly"
            self.create_pb_desktop()
        elif selected_item.get_string() == _["monthly"]:
            backup_item = "Monthly"
            self.create_pb_desktop()
        (width, height) = self.get_default_size()
        self.settings["window-size"] = (width, height)
        self.settings["maximized"] = self.is_maximized()
        self.settings["filename"] = self.saveEntry.get_text()
        self.settings["periodic-saving"] = backup_item
        if os.path.exists(f"{CACHE}/import_config/copying_flatpak_data"):
            print("Flatpak data exists.")
        elif os.path.exists(f"{CACHE}/syncing/copying_flatpak_data"):
            print("Flatpak data exists.")
        else:
            os.popen(f"rm -rf {CACHE}/periodic_saving")
            os.popen(f"rm -rf {CACHE}/syncing")
            os.popen(f"rm -rf {CACHE}/.*")
        try:
            url = urlopen(f"{self.settings['url-for-syncing']}/file-settings.json")
            j = json.load(url)
            if j["periodic-import"] == "Manually2":
                self.settings["manually-sync"] = True
            else:
                self.settings["manually-sync"] = False
            os.popen(f"rm {CACHE}/file-settings.json")
        except:
            self.settings["manually-sync"] = False
        
    ## Create desktop file to make periodic backups work
    def create_pb_desktop(self):
        if not os.path.exists(f'{home}/.config/autostart'):
            os.mkdir(f'{home}/.config/autostart')
        if not os.path.exists(f'{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop'):
            with open(f'{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop', 'w') as cb:
                cb.write(f'[Desktop Entry]\nName=SaveDesktop (Periodic backups)\nType=Application\nExec={periodic_saving_cmd}')
        
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")
        self.create_action('about', self.on_about_action, ["F1"])
        self.create_action('open-dir', self.open_dir)
        self.create_action('logout', self.logout)
        if self.settings["manually-sync"] == True:
            self.create_action('m_sync_with_key', self.sync_pc, ["<primary>s"])
        self.create_action('m_sync', self.sync_pc)
        self.create_action('quit', self.app_quit, ["<primary>q"])
        self.create_action('shortcuts', self.shortcuts, ["<primary>question"])
        self.connect('activate', self.on_activate)
        
    # Open directory (action after clicking button Open the folder on Adw.Toast)
    def open_dir(self, action, param):
        with open(f"{CACHE}/.filedialog.json") as fd:
            jf = json.load(fd)
        Gtk.FileLauncher.new(Gio.File.new_for_path(jf["recent_file"])).open_containing_folder()
    
    # Logout (action after clicking button Log Out on Adw.Toast)
    def logout(self, action, param):
        if snap:
            bus = dbus.SystemBus()
            systemd1 = bus.get_object("org.freedesktop.login1", "/org/freedesktop/login1")
            manager = dbus.Interface(systemd1, 'org.freedesktop.login1.Manager')
            sessions = manager.ListSessions()
            manager.KillSession(sessions[0][0], 'all', 9)
        else:
            if os.getenv('XDG_CURRENT_DESKTOP') == 'XFCE':
                os.system("dbus-send --session --type=method_call --print-reply --dest=org.xfce.SessionManager /org/xfce/SessionManager org.xfce.Session.Manager.Logout boolean:true boolean:false")
            elif os.getenv('XDG_CURRENT_DESKTOP') == 'KDE':
                os.system("dbus-send --print-reply --dest=org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout int32:0 int32:0 int32:0")
            else:
                os.system("dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1")

    # Sync config manually
    def sync_pc(self, action, param):
        if os.path.exists(f"{DATA}/sync-info.json"):
            os.remove(f"{DATA}/sync-info.json")
        os.system(f'notify-send "{_["please_wait"]}"')
        os.system(f"echo > {CACHE}/.from_app")
        self.sync_m = GLib.spawn_command_line_async(f"python3 {system_dir}/network_sharing.py")
        
    def shortcuts(self, action, param):
        shortcuts_window = ShortcutsWindow(
            transient_for=self.get_active_window())
        shortcuts_window.present()
        
    def app_quit(self, action, param):
        if os.path.exists(f"{CACHE}/import_config/copying_flatpak_data"):
            print("Flatpak data exists.")
        elif os.path.exists(f"{CACHE}/syncing/copying_flatpak_data"):
            print("Flatpak data exists.")
        else:     
            os.popen(f"rm -rf {CACHE}/*")
            os.popen(f"rm -rf {CACHE}/.*")
        app.quit()
        
    # About dialog
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("SaveDesktop")
        dialog.set_developer_name("vikdevelop")
        if not r_lang == "en":
            dialog.set_translator_credits(_["translator_credits"])
        print(lang_list)
        if not lang_list:
            dialog.add_link("Translate SaveDesktop Github Wiki", "https://hosted.weblate.org/projects/vikdevelop/savedesktop-github-wiki/")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/SaveDesktop")
        dialog.set_issue_url("https://github.com/vikdevelop/SaveDesktop/issues")
        dialog.set_copyright("© 2023-2024 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_artists(["Brage Fuglseth"])
        if os.path.exists("/app/share/build-beta.sh"):
            dialog.set_version(f"{version}-beta")
            dialog.set_application_icon(f"{icon}.Devel")
        else:
            dialog.set_version(version)
            dialog.set_application_icon(icon)
        dialog.set_release_notes(rel_notes)
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
