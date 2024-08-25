#!/usr/bin/python3
import os, socket, glob, sys, shutil, re, zipfile, random, string
from urllib.request import urlopen
from datetime import date
from pathlib import Path
from threading import Thread
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from localization import _, home
from open_wiki import *
from shortcuts_window import *

# Get user download dir
download_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)

# for SNAP: create the cache directory and import dbus module
if snap:
    import dbus
    os.makedirs(f"{CACHE}", exist_ok=True)

# load GSettings database for viewing and saving user settings of the app
settings = Gio.Settings.new_with_path("io.github.vikdevelop.SaveDesktop", "/io/github/vikdevelop/SaveDesktop/")

# Shortcuts window
@Gtk.Template(string=SHORTCUTS_WINDOW) # from shortcuts_window.py
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWindow'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Row for showing available apps
class FolderSwitchRow(Gtk.ListBoxRow):
    def __init__(self, folder_name):
        super().__init__()
        self.folder_name = folder_name
        
        # switch for all items
        self.switch = Gtk.Switch()
        self.switch.set_halign(Gtk.Align.END)
        self.switch.set_valign(Gtk.Align.CENTER)
        self.switch.connect("state-set", self.on_switch_activated)
        if settings["disabled-flatpak-apps-data"] == []:
            self.switch.set_active(True)
        
        # row for all items
        self.approw = Adw.ActionRow.new()
        self.approw.set_title(folder_name)
        self.approw.add_suffix(self.switch)
        self.approw.set_title_lines(4)
        self.approw.set_activatable_widget(self.switch)
        self.approw.set_hexpand(True)
        
        # box for self.approw
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.box.append(self.approw)
        
        self.set_child(self.box)
        
        # set switch states from the Gsettings database
        switch_state = folder_name not in settings.get_strv("disabled-flatpak-apps-data")
        self.switch.set_active(switch_state)
    
    # save switch state
    def on_switch_activated(self, switch, state):
        disabled_flatpaks = settings.get_strv("disabled-flatpak-apps-data")
        if not state:
            if self.folder_name not in disabled_flatpaks:
                disabled_flatpaks.append(self.folder_name)
        else:
            if self.folder_name in disabled_flatpaks:
                disabled_flatpaks.remove(self.folder_name)
        settings.set_strv("disabled-flatpak-apps-data", disabled_flatpaks)

# dialog for showing installed Flatpak apps
class FlatpakAppsDialog(Adw.MessageDialog):
    def __init__(self):
        super().__init__(transient_for=app.get_active_window())
        self.set_heading(_["flatpaks_data_tittle"])
        self.set_default_size(300, 400)
        
        # primary Gtk.Box for this dialog
        self.dialogBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_extra_child(self.dialogBox)
        
        self.old_disabled_flatpaks = settings["disabled-flatpak-apps-data"]
        
        # widget for scrolling items list
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_width(300)
        scrolled_window.set_min_content_height(380)
        self.dialogBox.append(scrolled_window)
        
        # listbox for showing items
        self.flowbox = Gtk.ListBox.new()
        self.flowbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.flowbox.add_css_class(css_class='boxed-list')
        
        # set self.flowbox as child for Gtk.ScrolledWindow widget
        scrolled_window.set_child(self.flowbox)
        
        # add buttons to the dialog
        self.add_response('cancel', _["cancel"])
        self.add_response('ok', _["apply"])
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.connect('response', self.apply_settings)
        
        # if there are problems loading a folder, an error message is displayed
        try:
            self.load_folders()
            self.set_initial_switch_state()
        except Exception as e:
            self.set_body(f"Error: {e}")
    
    # load items from ~/.var/app directory
    def load_folders(self):
        folder_path = f"{home}/.var/app"
        try:
            folder = Gio.File.new_for_path(folder_path)
            files = folder.enumerate_children("standard::name", Gio.FileQueryInfoFlags.NONE, None)
            while True:
                file_info = files.next_file(None)
                if file_info is None:
                    break
                folder_name = file_info.get_name()
                folder_row = FolderSwitchRow(folder_name)
                self.flowbox.append(folder_row)
        except Exception as e:
            print(f"Error loading folders: {e}")
       
    # set default switch state
    def set_initial_switch_state(self):
        disabled_flatpaks = settings.get_strv("disabled-flatpak-apps-data")
        for child in self.flowbox.get_row_at_index(0):
            if isinstance(child, FolderSwitchRow):
                child.switch.set_active(child.folder_name not in disabled_flatpaks)
    
    # if user clicks on the cancel button, the settings will not saved
    def apply_settings(self, w, response):
        if response == 'cancel':
            settings["disabled-flatpak-apps-data"] = self.old_disabled_flatpaks
    
# Application window
class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("SaveDesktop")
        self.application = kwargs.get('application')
        
        # header bar and toolbarview
        self.headerbar = Adw.HeaderBar.new()
        self.toolbarview = Adw.ToolbarView.new()
        self.toolbarview.add_top_bar(self.headerbar)
        
        # header bar for unsuppurtoed environment or disconnected some plugs in the Snap package
        self.errHeaderbar = Adw.HeaderBar.new()
        
        # values that set if state of the switch "Extensions" in the Items, state of the switch "User data of installed Flatpak apps will be saved or not", if whether whether to reopen the self.setDialog and if the Apply button in self.setDialog will be enabled or not
        self.save_ext_switch_state = self.flatpak_data_sw_state = self.open_setdialog_tf = self.set_button_sensitive = False
        
        # set the window size and maximization from the GSettings database
        (width, height) = settings["window-size"]
        self.set_default_size(width, height)
        
        # if value is TRUE, it enables window maximalization
        if settings["maximized"]:
            self.maximize()
        
        # App menu - primary menu
        self.main_menu = Gio.Menu()
        
        # primary menu section
        self.general_menu = Gio.Menu()
        self.general_menu.append(_["about_app"], 'app.about')
        self.general_menu.append(_["keyboard_shortcuts"], 'app.shortcuts')
        self.main_menu.append_section(None, self.general_menu)
        
        # menu button
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.main_menu)
        self.headerbar.pack_end(child=self.menu_button)
        
        # add Manually sync section
        if settings["manually-sync"] == True:
            self.sync_menu = Gio.Menu()
            self.sync_menu.append(_["sync"], 'app.m_sync_with_key')
            self.main_menu.append_section(None, self.sync_menu)
        
        # primary layout
        self.headapp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.headapp.set_valign(Gtk.Align.CENTER)
        self.headapp.set_halign(Gtk.Align.CENTER)
        self.toolbarview.set_content(self.headapp)
        
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
        self.syncingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Add pages to the menu switcher
        self.stack.add_titled_with_icon(self.saveBox,"savepage",_["save"],"document-save-symbolic")
        self.stack.add_titled_with_icon(self.importBox,"importpage",_["import_title"],"document-open-symbolic")
        self.stack.add_titled_with_icon(self.syncingBox,"syncpage",_["sync"],"emblem-synchronizing-symbolic")
        
        # menu switcher
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
        self.toast_overlay.set_child(self.toolbarview)
        self.set_content(self.toast_overlay)
        
        # Popup window for showing messages about saved and imported configuration
        self.toast = Adw.Toast.new(title='')
        self.toast.set_timeout(0)
        
        # Check the user's current desktop
        desktop_env = os.getenv('XDG_CURRENT_DESKTOP')
        desktop_map = {
            'GNOME': 'GNOME',
            'zorin:GNOME': 'GNOME',
            'ubuntu:GNOME': 'GNOME',
            'pop:GNOME': 'COSMIC (Old)',
            'COSMIC': 'COSMIC (New)',
            'Pantheon': 'Pantheon',
            'X-Cinnamon': 'Cinnamon',
            'Budgie:GNOME': 'Budgie',
            'XFCE': 'Xfce',
            'MATE': 'MATE',
            'KDE': 'KDE Plasma',
            'Deepin': 'Deepin'
        }

        # If the user has a supported environment, it shows the app window, otherwise, it shows the window with information about an unsupported environment
        def setup_environment(env_name):
            self.environment = env_name
            self.save_desktop()
            self.import_desktop()
            self.sync_desktop()
            self.connect("close-request", self.on_close)

        if desktop_env in desktop_map:
            setup_environment(desktop_map[desktop_env])
        else:
            # Handle unsupported desktop environments
            self.toolbarview.add_top_bar(self.errHeaderbar)
            self.toolbarview.remove(self.headerbar)
            self.toolbarview.set_content(self.pBox)
            self.pBox.set_margin_start(50)
            self.pBox.set_margin_end(50)
            self.pBox.append(Gtk.Image.new_from_icon_name("exclamation_mark"))
            self.pBox.append(Gtk.Label(str=_["unsuppurted_env_desc"].format("GNOME, Xfce, Budgie, Cinnamon, COSMIC, Pantheon, KDE Plasma, MATE, Deepin")).set_use_markup(True))

        # Show warning about disconnected plugs
        if snap:
            plugs = ["dot-config", "dot-local", "dot-themes", "dot-icons", "dot-fonts", "login-session-control"]
            show_warning = any(subprocess.run(["snapctl", "is-connected", plug], stdout=subprocess.PIPE).returncode != 0 for plug in plugs)

            if show_warning:
                self.toolbarview.add_top_bar(self.errHeaderbar)
                self.toolbarview.remove(self.headerbar)
                self.toolbarview.set_content(self.pBox)
                self.pBox.set_margin_start(90)
                self.pBox.set_margin_end(90)

                # Show warning message
                self.pBox.append(Gtk.Image.new_from_icon_name("exclamation_mark"))
                self.pBox.append(Gtk.Label(str="<big><b>Need to connect some plugs</b></big>\nIn order for SaveDesktop to work properly, you need to connect some plugs to access the files. You can do this by opening a terminal (Ctrl+Alt+T) and entering the following command: \n").set_use_markup(True))
                self.pBox.append(Gtk.Label(str="<i>sudo snap connect savedesktop:dot-config &amp;&amp; sudo snap connect savedesktop:dot-local &amp;&amp; sudo snap connect savedesktop:dot-themes &amp;&amp; sudo snap connect savedesktop:dot-icons &amp;&amp; sudo snap connect savedesktop:dot-fonts &amp;&amp; sudo snap connect savedesktop:login-session-control</i>").set_use_markup(True))
    
    # Show main page
    def save_desktop(self):
        # More options dialog
        def more_options_dialog(w):
            # create desktop file for enabling periodic saving at startup
            def create_pb_desktop():
                if not os.path.exists(f'{home}/.config/autostart'):
                    os.mkdir(f'{home}/.config/autostart')
                if not os.path.exists(f'{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop'):
                    with open(f'{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop', 'w') as cb:
                        cb.write(f'[Desktop Entry]\nName=SaveDesktop (Periodic backups)\nType=Application\nExec={periodic_saving_cmd}')
            
            # Action after closing dialog for showing more options
            def msDialog_closed(w, response):
                if response == 'ok':
                    settings["filename-format"] = self.filefrmtEntry.get_text()
                    settings["periodic-saving-folder"] = self.dirRow.get_subtitle()
                    settings["enable-encryption"] = self.encryptSwitch.get_active()
                    
                    selected_item = self.pbRow.get_selected_item()
                    backup_mapping = {_["never"]: "Never", _["daily"]: "Daily", _["weekly"]: "Weekly", _["monthly"]: "Monthly"}
                    backup_item = backup_mapping.get(selected_item.get_string(), "Never")

                    create_pb_desktop() if not backup_item == "Never" else None

                    settings["periodic-saving"] = backup_item

                    if self.open_setdialog_tf:
                        self.setDialog.close()
                        self.open_setDialog()

            # open a link to the wiki page about periodic saving
            def open_pb_wiki(w):
                os.system(f"xdg-open {pb_wiki}")

            # reset the file name format entry to the default value
            def reset_fileformat(w):
                self.filefrmtEntry.set_text("Latest_configuration")
            
            # Dialog for showing more options itself
            self.msDialog = Adw.MessageDialog.new(self)
            self.msDialog.set_default_size(400, 200)
            self.msDialog.set_heading(_["more_options"])

            # Box for this dialog
            self.msBox = Gtk.ListBox.new()
            self.msBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
            self.msBox.get_style_context().add_class(class_name='boxed-list')
            self.msDialog.set_extra_child(self.msBox)
            
            # Learn more about periodic saving
            self.pb_learnButton = Gtk.Button.new_from_icon_name("help-about-symbolic")
            self.pb_learnButton.set_tooltip_text(_["learn_more"])
            self.pb_learnButton.add_css_class("flat")
            self.pb_learnButton.set_valign(Gtk.Align.CENTER)
            self.pb_learnButton.connect("clicked", open_pb_wiki)
            
            # Periodic saving section
            # Expander row for showing options of the periodic saving
            self.saving_eRow = Adw.ExpanderRow.new()
            self.saving_eRow.set_title(_["periodic_saving"])
            self.saving_eRow.add_suffix(self.pb_learnButton)
            self.msBox.append(child=self.saving_eRow)
            
            options = Gtk.StringList.new(strings=[
                _["never"], _["daily"], _["weekly"], _["monthly"]
            ])
            
            self.pbRow = Adw.ComboRow.new()
            self.pbRow.set_title(_["pb_interval"])
            self.pbRow.set_use_markup(True)
            self.pbRow.set_subtitle(f"{_['periodic_saving_desc']}")
            self.pbRow.set_subtitle_lines(4)
            self.pbRow.set_model(model=options)
            self.saving_eRow.add_row(self.pbRow)
            
            # Load options from GSettings database
            if settings["periodic-saving"] == 'Never':
                self.pbRow.set_selected(0)
            elif settings["periodic-saving"] == 'Daily':
                self.pbRow.set_selected(1)
            elif settings["periodic-saving"] == 'Weekly':
                self.pbRow.set_selected(2)
            elif settings["periodic-saving"] == 'Monthly':
                self.pbRow.set_selected(3)
            
            # Restore filename format text to default
            self.filefrmtButton = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
            self.filefrmtButton.add_css_class('destructive-action')
            self.filefrmtButton.set_valign(Gtk.Align.CENTER)
            self.filefrmtButton.set_tooltip_text(_["reset_button"])
            self.filefrmtButton.connect("clicked", reset_fileformat)
            
            # Entry for selecting file name format
            self.filefrmtEntry = Adw.EntryRow.new()
            self.filefrmtEntry.set_title(_["filename_format"])
            self.filefrmtEntry.add_suffix(self.filefrmtButton)
            self.filefrmtEntry.set_text(settings["filename-format"])
            self.saving_eRow.add_row(self.filefrmtEntry)
            
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
            if settings["periodic-saving-folder"] == '':
                self.dirRow.set_subtitle(f"{download_dir}/SaveDesktop/archives")
            else:
                self.dirRow.set_subtitle(settings["periodic-saving-folder"])
            self.saving_eRow.add_row(self.dirRow)
                
            # Archive Encryption section
            # action row and switch for showing options of the archive encryption
            self.encryptSwitch = Gtk.Switch.new()
            self.encryptSwitch.set_valign(Gtk.Align.CENTER)
            if settings["enable-encryption"] == True:
                self.encryptSwitch.set_active(True)
            
            self.encryptRow = Adw.ActionRow.new()
            self.encryptRow.set_title(_["archive_encryption"])
            self.encryptRow.set_subtitle(f'{_["archive_encryption_desc"]} <a href="{enc_wiki}">{_["learn_more"]}</a>')
            self.encryptRow.set_subtitle_lines(5)
            self.encryptRow.add_suffix(self.encryptSwitch)
            self.encryptRow.set_activatable_widget(self.encryptSwitch)
            self.msBox.append(self.encryptRow)

            # add response of this dialog
            self.msDialog.add_response('cancel', _["cancel"])
            self.msDialog.add_response('ok', _["apply"])
            self.msDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
            self.msDialog.connect('response', msDialog_closed)
            
            self.msDialog.show()

        # =========
        # Save page

        # Open the More options dialog from the self.setDialog
        self.more_options_dialog = more_options_dialog
            
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
        self.saveEntry.set_text(settings["filename"])
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
        
        # section for showing dialog with more options
        # button
        self.msButton = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self.msButton.add_css_class('flat')
        self.msButton.set_valign(Gtk.Align.CENTER)
        self.msButton.connect("clicked", more_options_dialog)

        # action row
        self.moreSettings = Adw.ActionRow.new()
        self.moreSettings.set_title(_["more_options"])
        self.moreSettings.set_subtitle(f"{_['periodic_saving']}, {_['archive_encryption']}")
        self.moreSettings.add_suffix(self.msButton)
        self.moreSettings.set_activatable_widget(self.msButton)
        self.lbox_e.append(self.moreSettings)
        
        # Save configuration button
        self.saveButton = Gtk.Button.new_with_label(_["save"])
        self.saveButton.add_css_class("suggested-action")
        self.saveButton.add_css_class("pill")
        self.saveButton.connect("clicked", self.select_folder)
        self.saveButton.set_valign(Gtk.Align.CENTER)
        self.saveButton.set_halign(Gtk.Align.CENTER)
        self.saveBox.append(self.saveButton)
        
    # Import configuration page
    def import_desktop(self):
        # Import archive from list
        def import_from_list(w):
            # Action after closing import from list page
            def close_list(w):
                self.pBox.remove(self.flistBox)
                self.headerbar_list.remove(self.backButton)
                self.headerbar_list.remove(child=self.menu_button)
                self.headerbar.pack_end(child=self.menu_button)
                self.toolbarview.remove(self.headerbar_list)
                self.toolbarview.add_top_bar(self.headerbar)
                self.toolbarview.set_content(self.headapp)
                try:
                    self.headerbar.remove(self.applyButton)
                except:
                    pass
            
            # add back button for this page
            self.backButton = Gtk.Button.new_from_icon_name("go-next-symbolic-rtl")
            self.backButton.add_css_class("flat")
            self.backButton.connect("clicked", close_list)
            
            # remove main headerbar
            self.headerbar.remove(child=self.menu_button)
            self.toolbarview.remove(self.headerbar)
            
            # create new headerbar for this page
            self.headerbar_list = Adw.HeaderBar.new()
            self.headerbar_list.pack_start(self.backButton)
            self.headerbar_list.pack_end(child=self.menu_button)
            self.toolbarview.add_top_bar(self.headerbar_list)
            self.toolbarview.set_content(self.pBox)
            
            # set title for this page
            self.set_title(_["import_from_list"])
            
            # Box for this section
            self.flistBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
            self.pBox.append(self.flistBox)
            
            # Label for showing text in this section
            self.flistLabel = Gtk.Label.new()
            self.flistLabel.set_justify(Gtk.Justification.CENTER)
            if settings["periodic-saving-folder"] == '':
                self.dir = f'{download_dir}/SaveDesktop/archives'
            else:
                self.dir = f'{settings["periodic-saving-folder"]}'
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
                    self.headerbar_list.pack_end(self.applyButton)
                    
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

        # =======
        # Import page itself
        self.importBox.set_valign(Gtk.Align.CENTER)
        self.importBox.set_halign(Gtk.Align.CENTER)
        
        # Image and title for the Import page
        self.statusPage_i = Adw.StatusPage.new()
        self.statusPage_i.set_icon_name("document-open-symbolic")
        self.statusPage_i.set_title(_['import_config'])
        self.statusPage_i.set_description(_["import_config_desc"])
        #self.statusPage_i.set_child(self.syncingBox)
        self.importBox.append(self.statusPage_i)
        
        # Box of Import from file and Import from list buttons
        self.importbtnBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=7)
        self.importbtnBox.set_halign(Gtk.Align.CENTER)
        self.importBox.append(self.importbtnBox)
        
        # Import configuration button
        self.fileButton = Gtk.Button.new_with_label(_["import_from_file"])
        self.fileButton.add_css_class("pill")
        self.fileButton.add_css_class("suggested-action")
        self.fileButton.connect("clicked", self.select_folder_to_import)
        self.importbtnBox.append(self.fileButton)
        
        # Import from list button
        self.fromlistButton = Gtk.Button.new_with_label(_["import_from_list"])
        self.fromlistButton.add_css_class("pill")
        self.fromlistButton.connect("clicked", import_from_list)
        self.importbtnBox.append(self.fromlistButton)
            
    # Syncing desktop page
    def sync_desktop(self):
        self.syncingBox.set_valign(Gtk.Align.CENTER)
        self.syncingBox.set_halign(Gtk.Align.CENTER)
        self.syncingBox.set_margin_start(40)
        self.syncingBox.set_margin_end(40)

        # Image and title for this page
        self.statusPage = Adw.StatusPage.new()
        self.statusPage.set_icon_name("emblem-synchronizing-symbolic")
        self.statusPage.set_title(_["sync_title"])
        self.statusPage.set_description(f'{_["sync_desc"]} <a href="{sync_wiki}">{_["learn_more"]}</a>')
        #self.statusPage.set_child(self.syncingBox)
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
        # copy the sync file to the app data folder for proper funcionality
        def copy_sync_file():
            try:
                if not os.path.exists(f"{DATA}/synchronization"):
                    os.mkdir(f"{DATA}/synchronization")
                if not os.path.exists(f"{DATA}/synchronization/{settings['filename-format']}.sd.tar.gz"):
                    os.chdir(f"{DATA}/synchronization")
                    os.system(f"rm *.sd.tar.gz")
                    shutil.copyfile(self.file_row.get_subtitle(), f"{DATA}/synchronization/{settings['filename-format']}.sd.tar.gz")
            except Exception as e:
                os.system(f"notify-send 'An error occured' '{e}'")
            finally:
                print("The sync file has been copied to the SaveDesktop data folder successfully.")

        # Create periodic saving file if it does not exist
        def save_now():
            try:
                subprocess.run(['notify-send', 'SaveDesktop', _["please_wait"]])
                self.file_row.set_use_markup(False)
                subprocess.run([f"{system_dir}/bin/run.sh", "--save-now"] if (flatpak or snap) else ["savedesktop", "--save-now"], check=True)
            except subprocess.CalledProcessError as e:
                subprocess.run(subprocess.run(['notify-send', 'An error occurred', str(e.stderr)]))
            finally:
                self.file_row.remove(self.setupButton)
                self.file_row.set_subtitle(f'{settings["periodic-saving-folder"]}/{settings["filename-format"]}.sd.tar.gz')
                os.system(f"notify-send 'SaveDesktop' '{_['config_saved']}'")
                self.setDialog.set_response_enabled('ok', True)
                
        def make_pb_file(w):
            self.setupButton.set_sensitive(False)
            pb_thread = Thread(target=save_now)
            pb_thread.start()
        
        # Action after closing dialog for setting synchronization file
        def setDialog_closed(w, response):
            if response == 'ok':
                self.open_setdialog_tf = False
                self.set_syncing()
                
                if "fuse" in subprocess.getoutput(f"df -T \"{self.file_row.get_subtitle()}\""):
                    open(f"{settings['periodic-saving-folder']}/SaveDesktop.json", "w").write('{\n "periodic-saving-interval": "%s",\n "periodic-saving-folder": "%s",\n "filename": "%s.sd.tar.gz"\n}' % (settings["periodic-saving"], settings["periodic-saving-folder"], settings["filename-format"]))
                    self.set_up_auto_mount()
                else:
                    # start copying the synchronization file process
                    setup_thread = Thread(target=copy_sync_file)
                    setup_thread.start()
                    
                    # Check if the Python HTTP Server is running - if not, it shows popup window of the need to log out of the system
                    if "Couldn't connect to server" in subprocess.getoutput(f"curl --head --fail {self.url_row.get_subtitle()}"):
                        if not settings["periodic-saving"] == 'Never':
                            self.show_warn_toast()
            else:
                self.open_setdialog_tf = False

        # self.setDialog
        self.setDialog = Adw.MessageDialog.new(self)
        self.setDialog.set_heading(_["set_up_sync_file"])
        self.setDialog.set_body_use_markup(True)
        self.setDialog.set_default_size(450, 200)

        # Check periodic saving file path and existence
        path = f'{settings["periodic-saving-folder"]}/{settings["filename-format"]}.sd.tar.gz' if "onedrive" in settings["periodic-saving-folder"] else f'{settings["periodic-saving-folder"]}/{settings["filename-format"]}.sd.tar.gz'.replace(" ", "_")
        folder = (f'<span color="red">{_["pb_interval"]}: {_["never"]}</span>' 
                  if settings["periodic-saving"] == "Never" 
                  else path if os.path.exists(path) 
                  else f'<span color="red">Periodic saving file does not exist.</span>')
        
        check_filesystem = subprocess.getoutput(f"df -T \"{settings['periodic-saving-folder']}\"")
        
        self.set_button_sensitive = settings["periodic-saving"] != "Never" and not os.path.exists(path)

        # List Box for appending widgets
        self.l_setdBox = Gtk.ListBox.new()
        self.l_setdBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.l_setdBox.get_style_context().add_class('boxed-list')
        self.setDialog.set_extra_child(self.l_setdBox)

        # Row for showing selected synchronization file
        self.file_row = Adw.ActionRow.new()
        self.file_row.set_title(_["periodic_saving_file"])
        self.file_row.set_subtitle(folder)
        self.file_row.add_suffix(Gtk.Image.new_from_icon_name("network-wired-symbolic")) if "fuse" in check_filesystem and not "red" in folder else None
        self.file_row.set_subtitle_lines(4)
        self.file_row.set_use_markup(True)
        self.file_row.set_subtitle_selectable(True)
        self.l_setdBox.append(self.file_row)

        # Button for creating a periodic saving file if it does not exist
        if "Periodic saving file does not exist." in folder:
            self.setupButton = Gtk.Button.new_with_label("Create")
            self.setupButton.set_valign(Gtk.Align.CENTER)
            self.setupButton.add_css_class("suggested-action")
            self.setupButton.connect("clicked", make_pb_file)
            self.file_row.add_suffix(self.setupButton)

        # Button for opening More options dialog
        self.open_setdialog_tf = True
        self.ps_button = Gtk.Button.new_with_label("Change")
        self.ps_button.connect('clicked', self.more_options_dialog)
        self.ps_button.set_valign(Gtk.Align.CENTER)

        # Row for showing the selected periodic saving interval
        ## translate the periodic-saving key to the user language
        pb = next((key for key, value in {_["never"]: "Never", _["daily"]: "Daily", _["weekly"]: "Weekly", _["monthly"]: "Monthly"}.items() if settings["periodic-saving"] == value), None)
        self.ps_row = Adw.ActionRow.new()
        self.ps_row.set_title(f'{_["periodic_saving"]} ({_["pb_interval"]})')
        self.ps_row.set_use_markup(True)
        self.ps_row.add_suffix(self.ps_button)
        self.ps_row.set_subtitle(f'<span color="red">{_["never"]}</span>' if settings["periodic-saving"] == "Never" 
                                 else f'<span color="green">{pb}</span>')
        self.ps_button.add_css_class('suggested-action') if settings["periodic-saving"] == "Never" else None
        self.l_setdBox.append(self.ps_row)

        # Action row for showing URL for synchronization
        self.url_row = Adw.ActionRow.new()
        self.url_row.set_title(_["url_for_sync"])
        self.url_row.set_use_markup(True)
        self.url_row.set_subtitle(f"<span color='red'>{IPAddr}</span>" if "ERR:" in IPAddr 
                                  else f"http://{IPAddr}:8000/{settings['filename-format']}.sd.tar.gz")
        self.url_row.set_subtitle_selectable(True)

        # Append URL row if conditions are met
        if not ("red" in folder or "fuse" in check_filesystem):
            self.l_setdBox.append(self.url_row)

        # Dialog responses
        self.setDialog.add_response('cancel', _["cancel"])
        self.setDialog.add_response('ok', _["apply"])
        self.setDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        if "red" in folder:
            self.setDialog.set_response_enabled('ok', False)
        self.setDialog.connect('response', setDialog_closed)

        self.setDialog.show()

    # URL Dialog (action after clicking on the "Connect with other computer" button)
    def open_urlDialog(self, w):
        self.urlDialog_fnc()

    # URL Dialog iself
    def urlDialog_fnc(self):
        # if self.urlEntry is not empty, it enables the Apply button
        def enable_response_urlEntry(urlEntry):
            if not self.urlEntry.get_text() == "":
                self.urlDialog.set_response_enabled('ok', True)
            else:
                self.urlDialog.set_response_enabled('ok', False)
        
        # reset the cloud folder selection to the default value
        def reset_cloud_folder(w):
            self.cfileRow.set_subtitle("")
            self.cfileRow.remove(self.resetButton)
            self.urlDialog.set_response_enabled('ok', True)
            settings["file-for-syncing"] = self.cfileRow.get_subtitle()
        
        # Action after closing URL dialog
        def urlDialog_closed(w, response):
            if response == 'ok':
                check_psync = settings["periodic-import"]
                
                # translate the periodic sync options to English
                selected_item = self.psyncRow.get_selected_item()
                sync = {_["never"]: "Never2", _["manually"]: "Manually2", _["daily"]: "Daily2", _["weekly"]: "Weekly2", _["monthly"]: "Monthly2"}
                
                sync_item = sync.get(selected_item.get_string(), "Never2")

                settings["periodic-import"] = sync_item
                
                # if the selected periodic saving interval is "Manually2", it enables the manually-sync value
                settings["manually-sync"] = True and settings["periodic-import"] == "Manually2"
                
                # if it is selected to manually sync, it creates an option in the app menu in the header bar
                if settings["manually-sync"]:
                    self.sync_menu = Gio.Menu()
                    self.sync_menu.append(_["sync"], 'app.m_sync_with_key')
                    self.main_menu.append_section(None, self.sync_menu)
                    self.sync_menu.remove(1)
                    self.show_special_toast()
                else:
                    try:
                        self.sync_menu.remove(0)
                    except:
                        pass  # silently handle the exception
                    
                    # check if the selected periodic sync interval was Never: if yes, shows the message about the necessity to log out of the system
                    if check_psync == "Never2":
                        if not settings["periodic-import"] == "Never2":
                            self.show_warn_toast()

                # Set up cloud sync
                cfile_subtitle = self.cfileRow.get_subtitle()
                if cfile_subtitle:
                    self.set_up_auto_mount()
                        
                    # Check if the selected cloud drive folder is correct
                    if "fuse" in subprocess.getoutput(f"df -T \"{cfile_subtitle}\""):
                        settings["file-for-syncing"] = cfile_subtitle
                    else:
                        os.system("notify-send 'An error occured' 'You did not select the cloud drive folder!'")
                        settings["file-for-syncing"] = ""
                    settings["url-for-syncing"] = ""

                # Set up local network sync
                elif (url := self.urlEntry.get_text()):
                    settings["url-for-syncing"] = url
                    try:
                        urlopen(url)  # Check if the URL is correct
                        self.set_syncing()
                        self.show_warn_toast()
                    except Exception as e:
                        err = str(e).replace("<", "").replace(">", "") if "<" in str(e) else str(e)
                        os.system(f"notify-send 'SaveDesktop' 'ERR: {err}'")
                        settings["url-for-syncing"] = ""
                    settings["file-for-syncing"] = ""
                else:
                    print("Nothing changed.")

        # self.urlDialog
        self.urlDialog = Adw.MessageDialog.new(self)
        self.urlDialog.set_heading(_["connect_with_other_computer"])
        self.urlDialog.set_default_size(500,370)
          
        # Box for adding widgets in this dialog
        self.urlBox = Gtk.ListBox.new()
        self.urlBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.urlBox.get_style_context().add_class(class_name='boxed-list')
        self.urlDialog.set_extra_child(self.urlBox)
        
        # Row for connecting to computer in the local network
        self.localRow = Adw.ExpanderRow.new()
        self.localRow.set_title("Connect to computer in the local network")
        self.localRow.set_subtitle(_["connect_with_pc_desc"])
        self.localRow.set_subtitle_lines(6)
        self.urlBox.append(self.localRow)

        # Entry for entering the URL for synchronization
        self.urlEntry = Adw.EntryRow.new()
        self.urlEntry.set_title(_["pc_url_entry"])
        self.urlEntry.connect("changed", enable_response_urlEntry)
        self.urlEntry.set_text(settings["url-for-syncing"])
        self.localRow.add_row(self.urlEntry)
        
        # Row for connecting cloud drive
        self.cloudRow = Adw.ExpanderRow.new()
        self.cloudRow.set_title("Connect with the cloud storage")
        self.cloudRow.set_subtitle("On another computer, open the SaveDesktop app, and on this page, click on the \"Set up the sync file\" button and make the necessary settings. On this computer, select the folder that you have synced with your cloud storage and also have saved the same periodic saving file.")
        self.cloudRow.set_subtitle_lines(6)
        self.urlBox.append(self.cloudRow)
        
        # Row and buttons for selecting the cloud drive folder
        ## button for selecting the cloud drive folder
        self.cloudButton = Gtk.Button.new_from_icon_name("document-open-symbolic")
        self.cloudButton.add_css_class('flat')
        self.cloudButton.set_valign(Gtk.Align.CENTER)
        self.cloudButton.set_tooltip_text(_["set_another"])
        self.cloudButton.connect("clicked", self.select_sync_file)
        
        ## button for reseting the selected cloud drive folder
        self.resetButton = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        self.resetButton.add_css_class('destructive-action')
        self.resetButton.connect("clicked", reset_cloud_folder)
        self.resetButton.set_tooltip_text(_["reset_button"])
        self.resetButton.set_valign(Gtk.Align.CENTER)
        
        ## the row itself
        self.cfileRow = Adw.ActionRow.new()
        
        settings["file-for-syncing"] = "" if "sd.tar.gz" in settings["file-for-syncing"] else settings["file-for-syncing"]
        
        ### add the reset button if the subtitle is not empty
        self.cfileRow.add_suffix(self.resetButton) if not settings["file-for-syncing"] == "" else None
        
        self.cfileRow.set_title("Select cloud drive folder")
        self.cfileRow.set_subtitle(settings["file-for-syncing"])
        self.cfileRow.set_subtitle_selectable(True)
        self.cfileRow.add_suffix(self.cloudButton)
        self.cfileRow.set_activatable_widget(self.cloudButton)
        self.cloudRow.add_row(self.cfileRow)
        
        # Periodic sync section
        options = Gtk.StringList.new(strings=[
           _["never"], _["manually"], _["daily"], _["weekly"], _["monthly"]
        ])
        
        self.psyncRow = Adw.ComboRow.new()
        self.psyncRow.set_use_markup(True)
        self.psyncRow.set_use_underline(True)
        self.psyncRow.set_title(_["periodic_sync"])
        self.psyncRow.set_title_lines(2)
        self.psyncRow.set_model(model=options)
        self.urlBox.append(self.psyncRow)

        # Load periodic sync values form GSettings database
        if settings["periodic-import"] == "Never2":
            self.psyncRow.set_selected(0)
        elif settings["periodic-import"] == "Manually2":
            self.psyncRow.set_selected(1)
        elif settings["periodic-import"] == "Daily2":
            self.psyncRow.set_selected(2)
        elif settings["periodic-import"] == "Weekly2":
            self.psyncRow.set_selected(3)
        elif settings["periodic-import"] == "Monthly2":
            self.psyncRow.set_selected(4)
        
        self.urlDialog.add_response('cancel', _["cancel"])
        self.urlDialog.add_response('ok', _["apply"])
        self.urlDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        if not self.urlEntry.get_text() and not self.cfileRow.get_subtitle():
            self.urlDialog.set_response_enabled('ok', False)
        else:
            self.urlDialog.set_response_enabled('ok', True)
        self.urlDialog.connect('response', urlDialog_closed)
        self.urlDialog.show()

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
      
    # set up auto-mounting of the cloud drives after logging in to the system
    def set_up_auto_mount(self):
        try:
            cfile_subtitle = self.fileRow.get_subtitle()
        except:
            cfile_subtitle = settings["periodic-saving-folder"]
        if settings["periodic-import"] != "Manually2" and "gvfs" in cfile_subtitle:
            pattern = r'.*/gvfs/([^:]*):host=([^,]*),user=([^/]*).*' if "onedrive" not in cfile_subtitle else r'.*/gvfs/([^:]*):host=([^/]*).*'
            match = re.search(pattern, cfile_subtitle)

            if match:
                cloud_service = match.group(1)
                host = match.group(2)
                user = match.group(3) if "onedrive" not in cfile_subtitle else None
                
                with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.MountDrive.desktop", "w") as m:
                    m.write(f"[Desktop Entry]\nName=SaveDesktop (Mount Cloud Drive)\nType=Application\nExec=gio mount {cloud_service}://{user}@{host}") if not "onedrive" in cfile_subtitle else m.write(f"[Desktop Entry]\nName=SaveDesktop (Mount Cloud Drive)\nType=Application\nExec=gio mount {cloud_service}://{host}")
            else:
                print("Failed to extract the necessary values to set up automatic cloud storage connection after logging into the system.")
        elif "rclone" in subprocess.getoutput(f"df -T {cfile_subtitle}"):
            with open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.MountDrive.desktop", "w") as m:
                m.write(f"[Desktop Entry]\nName=SaveDesktop (Mount Cloud Drive)\nType=Application\nExec=rclone mount {cfile_subtitle.split('/')[-1]}: {cfile_subtitle.split('/')[-1]}")
    
    # Dialog: items to include in the configuration archive
    def open_itemsDialog(self, w):
        # Action after closing itemsDialog
        def itemsdialog_closed(w, response):
            if response == 'ok':
                # Saving the selected options to GSettings database
                settings["save-icons"] = self.switch_01.get_active()
                settings["save-themes"] = self.switch_02.get_active()
                settings["save-fonts"] = self.switch_03.get_active()
                settings["save-backgrounds"] = self.switch_04.get_active()
                settings["save-desktop-folder"] = self.switch_de.get_active()
                if flatpak:
                    settings["save-installed-flatpaks"] = self.switch_05.get_active()
                    settings["save-flatpak-data"] = self.switch_06.get_active()
                if self.save_ext_switch_state == True:
                    settings["save-extensions"] = self.switch_ext.get_active()
                    self.save_ext_switch_state = False
            elif response == 'cancel':
                switch_status = self.flatpak_data_sw_state
                settings["save-flatpak-data"] = switch_status

        # show dialog for managing Flatpak applications data
        def manage_data_list(w):
            self.itemsDialog.close()
            self.appd = FlatpakAppsDialog()
            self.appd.show()

        # show button after clicking on the switch "User data of Flatpak apps"
        def show_appsbtn(w, GParamBoolean):
            self.flatpak_data_sw_state = settings["save-flatpak-data"]
            if self.switch_06.get_active() == True:
                self.data_row.add_suffix(self.appsButton)
            else:
                self.data_row.remove(self.appsButton)
            settings["save-flatpak-data"] = self.switch_06.get_active()

        # show extensions row, if user has installed GNOME, Cinnamon or KDE Plasma DE
        def show_extensions_row():
            # Switch and row of option 'Save extensions'
            self.switch_ext = Gtk.Switch.new()
            if settings["save-extensions"]:
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

        # self.itemsDialog
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
        if settings["save-icons"]:
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
        if settings["save-themes"]:
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
        if settings["save-fonts"]:
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
        if settings["save-backgrounds"]:
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
        
        # show extension switch and row if user has installed these environments
        if self.environment in ["GNOME", "KDE Plasma", "Cinnamon", "COSMIC (Old)"]:
            self.save_ext_switch_state = True
            show_extensions_row()
        
        # Switch and row of option 'Save Desktop' (~/Desktop)
        self.switch_de = Gtk.Switch.new()
        if settings["save-desktop-folder"]:
            self.switch_de.set_active(True)
        self.switch_de.set_valign(align=Gtk.Align.CENTER)
        
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
            if settings["save-installed-flatpaks"]:
                self.switch_05.set_active(True)
            self.switch_05.set_valign(align=Gtk.Align.CENTER)
            
            self.list_row = Adw.ActionRow.new()
            self.list_row.set_title(title=_["list"])
            self.list_row.set_use_markup(True)
            self.list_row.set_title_lines(4)
            self.list_row.add_suffix(self.switch_05)
            self.list_row.set_activatable_widget(self.switch_05)
            self.flatpak_row.add_row(child=self.list_row)
            
            # Switch, button and row of option 'Save SaveDesktop app settings'
            self.switch_06 = Gtk.Switch.new()
            self.appsButton = Gtk.Button.new_from_icon_name("go-next-symbolic")
            
            self.data_row = Adw.ActionRow.new()
            self.data_row.set_title(title=_["user_data_flatpak"])
            self.data_row.set_use_markup(True)
            self.data_row.set_title_lines(4)
            self.data_row.add_suffix(self.switch_06)
            self.data_row.set_activatable_widget(self.switch_06)
            self.flatpak_row.add_row(child=self.data_row)
            
            if settings["save-flatpak-data"]:
                self.switch_06.set_active(True)
                self.data_row.add_suffix(self.appsButton)
            self.flatpak_data_sw_state = settings["save-flatpak-data"]
            self.switch_06.set_valign(align=Gtk.Align.CENTER)
            self.switch_06.connect('notify::active', show_appsbtn)
            
            self.appsButton.add_css_class("flat")
            self.appsButton.set_valign(Gtk.Align.CENTER)
            self.appsButton.set_tooltip_text(_["flatpaks_data_tittle"])
            self.appsButton.connect("clicked", manage_data_list)
        
        self.itemsDialog.add_response('cancel', _["cancel"])
        self.itemsDialog.add_response('ok', _["apply"])
        self.itemsDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.itemsDialog.connect('response', itemsdialog_closed)
        self.itemsDialog.show()
    
    # Select folder for periodic backups (Gtk.FileDialog)
    def select_pb_folder(self, w):
        def save_selected(source, res, data):
            try:
                file = source.select_folder_finish(res)
            except:
                return
            self.folder_pb = file.get_path()
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
            self.folder = file.get_path()
            if settings["enable-encryption"] == True:
                self.create_password_dialog()
            else:
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
    def select_folder_to_import(self, w):
        def open_selected(source, res, data):
            try:
                file = source.open_finish(res)
            except:
                return
            with open(f"{CACHE}/.impfile.json", "w") as j:
                j.write('{\n "import_file": "%s"\n}' % file.get_path())
            if ".zip" in file.get_path():
                self.check_password_dialog()
            else:
                self.please_wait_import()
                self.import_config()
        
        self.file_chooser = Gtk.FileDialog.new()
        self.file_chooser.set_modal(True)
        self.file_chooser.set_title(_["import_fileshooser"].format(self.environment))
        self.file_filter = Gtk.FileFilter.new()
        self.file_filter.set_name(_["savedesktop_f"])
        self.file_filter.add_pattern('*.sd.tar.gz')
        self.file_filter.add_pattern('*.sd.zip')
        self.file_filter_list = Gio.ListStore.new(Gtk.FileFilter);
        self.file_filter_list.append(self.file_filter)
        self.file_chooser.set_filters(self.file_filter_list)
        self.file_chooser.open(self, None, open_selected, None)
        
    # Select file for syncing cfg with other computers in the network
    def select_sync_file(self, w):
        def set_selected(source, res, data):
            try:
                file = source.select_folder_finish(res)
            except:
                return
            self.syncfile = file.get_path()
            self.cfileRow.set_subtitle(self.syncfile)
            self.urlDialog.set_response_enabled('ok', True)
            
        self.syncfile_chooser = Gtk.FileDialog.new()
        self.syncfile_chooser.set_modal(True)
        self.syncfile_chooser.set_title("Select cloud drive folder")
        self.syncfile_chooser.select_folder(self, None, set_selected, None)
        
    # Dialog for creating password for the config archive
    def create_password_dialog(self):
        # Action after closing pswdDialog
        def pswdDialog_closed(w, response):
            if response == 'ok':
                with open(f"{CACHE}/.pswd_temp", "w") as p:
                    p.write(self.pswdEntry.get_text())
                self.save_config()

        # Check the password to see if it meets the criteria
        def check_password(pswdEntry):
            password = self.pswdEntry.get_text()
            criteria = [
                (len(password) < 12, "The password is too short. It should has at least 12 characters"),
                (not re.search(r'[A-Z]', password), "The password should has at least one capital letter"),
                (not re.search(r'[a-z]', password), "The password should has at least one lowercase letter"),
                (not re.search(r'[@#$%^&*()":{}|<>_-]', password), "The password should has at least one special character"),
                (" " in password, "The password must not contain spaces")
            ]
            
            for condition, message in criteria:
                if condition:
                    self.pswdDialog.set_response_enabled("ok", False)
                    print(message)
                    return
                    
            self.pswdDialog.set_response_enabled("ok", True)

        # Generate Password
        def pswd_generator(w):
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(24))
            self.pswdEntry.set_text(password)

        # dialog itself
        self.pswdDialog = Adw.MessageDialog.new(self)
        self.pswdDialog.set_heading(_["create_pwd_title"])
        self.pswdDialog.set_body(_["create_pwd_desc"])

        # button for generating strong password
        self.pswdgenButton = Gtk.Button.new_from_icon_name("emblem-synchronizing-symbolic")
        self.pswdgenButton.set_tooltip_text("Generate Password")
        self.pswdgenButton.add_css_class("flat")
        self.pswdgenButton.set_valign(Gtk.Align.CENTER)
        self.pswdgenButton.connect("clicked", pswd_generator)

        # entry for entering password
        self.pswdEntry = Adw.PasswordEntryRow.new()
        self.pswdEntry.set_title(_["password_entry"])
        self.pswdEntry.connect('changed', check_password)
        self.pswdEntry.add_suffix(self.pswdgenButton)
        self.pswdDialog.set_extra_child(self.pswdEntry)

        self.pswdDialog.add_response("cancel", _["cancel"])
        self.pswdDialog.add_response("ok", _["apply"])
        self.pswdDialog.set_response_enabled("ok", False)
        self.pswdDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.pswdDialog.connect('response', pswdDialog_closed)
        self.pswdDialog.show()
    
    # Save configuration
    def save_config(self):
        self.please_wait_save()
        if settings["enable-encryption"] == True:
            with open(f"{CACHE}/.filedialog.json", "w") as w:
                w.write('{\n "recent_file": "%s/%s.sd.zip"\n}' % (self.folder, self.filename_text))
        else:
            with open(f"{CACHE}/.filedialog.json", "w") as w:
                w.write('{\n "recent_file": "%s/%s.sd.tar.gz"\n}' % (self.folder, self.filename_text))
        if not os.path.exists(f"{CACHE}/save_config"):
            os.mkdir(f"{CACHE}/save_config")
        os.chdir(f"{CACHE}/save_config")
        save_thread = Thread(target=self.start_saving)
        save_thread.start()
        
    # start process of saving the configuration
    def start_saving(self):
        try:
            e_o = False
            from config import Save
            Save()
        except Exception as e:
            e_o = True
            error = e
            GLib.idle_add(self.show_err_msg, error)
            self.toolbarview.set_content(self.headapp)
            self.toolbarview.remove(self.headerbar_save)
            self.toolbarview.add_top_bar(self.headerbar)
        finally:
            if not e_o:
                self.exporting_done()
            
    # "Please wait" information page on the "Save" page
    def please_wait_save(self):
        # Stop saving configuration
        def cancel_save(w):
            os.system(f"pkill -xf 'python3 {system_dir}/config.py --save'")
            self.toolbarview.set_content(self.headapp)
            self.toolbarview.remove(self.headerbar_save)
            self.toolbarview.add_top_bar(self.headerbar)
            for widget in [self.savewaitSpinner, self.savewaitLabel, self.savewaitButton, self.sdoneImage, self.opensaveButton, self.backtomButton]:
                self.savewaitBox.remove(widget)

        # Add headerbar for this page
        self.headerbar_save = Adw.HeaderBar.new()
        self.headerbar_save.pack_end(self.menu_button)
        self.toolbarview.add_top_bar(self.headerbar_save)
        self.toolbarview.remove(self.headerbar)

        # Create box widget for this page
        self.savewaitBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.savewaitBox.set_halign(Gtk.Align.CENTER)
        self.savewaitBox.set_valign(Gtk.Align.CENTER)
        self.toolbarview.set_content(self.savewaitBox)

        # Set bold title
        self.set_title(_["saving_config_status"].split('</b>')[0].split('<b>')[-1])

        # Create spinner for this page
        self.savewaitSpinner = Gtk.Spinner.new()
        self.savewaitSpinner.set_size_request(100, 100)
        self.savewaitSpinner.start()
        self.savewaitBox.append(self.savewaitSpinner)

        # Prepare Gtk.Image widget for the next page
        self.sdoneImage = Gtk.Image.new()
        self.savewaitBox.append(self.sdoneImage)

        # Use "sd.zip" if Archive Encryption is enabled
        status = _["saving_config_status"].replace("sd.tar.gz", "sd.zip") if settings["enable-encryption"] else _["saving_config_status"]

        # Create label about selected directory for saving the configuration
        self.savewaitLabel = Gtk.Label.new(str=status.format(self.folder, self.filename_text))
        self.savewaitLabel.set_use_markup(True)
        self.savewaitLabel.set_justify(Gtk.Justification.CENTER)
        self.savewaitLabel.set_wrap(True)
        self.savewaitBox.append(self.savewaitLabel)

        # Create button for cancel saving configuration
        self.savewaitButton = Gtk.Button.new_with_label(_["cancel"])
        self.savewaitButton.add_css_class("pill")
        self.savewaitButton.add_css_class("destructive-action")
        self.savewaitButton.connect("clicked", cancel_save)
        self.savewaitButton.set_margin_start(170)
        self.savewaitButton.set_margin_end(170)
        self.savewaitBox.append(self.savewaitButton)
        
    # config has been saved action
    def exporting_done(self):
        # back to the previous page from this page
        def back_to_main(w):
            self.toolbarview.set_content(self.headapp)
            self.toolbarview.remove(self.headerbar_save)
            self.toolbarview.add_top_bar(self.headerbar)
            
            for widget in [self.savewaitSpinner, self.savewaitLabel, self.savewaitButton, self.sdoneImage, self.opensaveButton, self.backtomButton]:
                self.savewaitBox.remove(widget)
        
        # send notification about saved configuration if application window is inactive only
        self.notification_save = Gio.Notification.new("SaveDesktop")
        self.notification_save.set_body(_["config_saved"])
        active_window = app.get_active_window()
        if active_window is None or not active_window.is_active():
            app.send_notification(None, self.notification_save)
        
        # stop spinner animation
        self.savewaitSpinner.stop()
        self.savewaitBox.remove(self.savewaitButton)

        # set title to "Configuration has been saved!"
        self.set_title(_['config_saved'])

        # use widget for showing done.svg icon
        self.sdoneImage.set_from_icon_name("done")
        self.sdoneImage.set_pixel_size(128)

        # edit label for the purposes of this page
        self.savewaitLabel.set_label(_["config_saved_desc"].format(_['config_saved']))
        self.opensaveButton = Gtk.Button.new_with_label(_["open_folder"])
        self.opensaveButton.add_css_class('pill')
        self.opensaveButton.add_css_class('suggested-action')
        self.opensaveButton.set_action_name('app.open-dir')
        self.opensaveButton.set_margin_start(170)
        self.opensaveButton.set_margin_end(170)
        self.savewaitBox.append(self.opensaveButton)

        # create button for backing to the previous page
        self.backtomButton = Gtk.Button.new_with_label(_["back_to_page"])
        self.backtomButton.connect("clicked", back_to_main)
        self.backtomButton.add_css_class("pill")
        self.backtomButton.set_margin_start(170)
        self.backtomButton.set_margin_end(170)
        self.savewaitBox.append(self.backtomButton)
        
        # remove content in the cache directory
        os.popen(f"rm -rf {CACHE}/save_config/")
        os.popen(f"rm {CACHE}/.pswd_temp")
    
    # Import config from list
    def imp_cfg_from_list(self, w):
        selected_archive = self.radio_row.get_selected_item()
        with open(f"{CACHE}/.impfile.json", "w") as j:
            j.write('{\n "import_file": "%s/%s"\n}' % (self.dir, selected_archive.get_string()))
        if not os.path.exists(f"{CACHE}/import_from_list"):
            os.mkdir(f"{CACHE}/import_from_list")
        os.chdir(f"{CACHE}/import_from_list")
        self.please_wait_import()
        import_thread = Thread(target=self.start_importing)
        import_thread.start()
     
    # dialog for entering password of the archive
    def check_password_dialog(self):
        # unzip archive if password is correct only
        def unzip_ar():
            with open(f"{CACHE}/.impfile.json") as i:
                j = json.load(i)
            if not os.path.exists(f"{CACHE}/import_config"):
                os.mkdir(f"{CACHE}/import_config")
            file_name = j["import_file"]
            self.please_wait_import()
            try:
                e_o = False
                with zipfile.ZipFile(file_name, "r") as zip:
                    zip.extractall(path=f"{CACHE}/import_config", pwd=f"{self.checkEntry.get_text()}".encode("utf-8"))
            except Exception as err:
                e_o = True
                error = err
                GLib.idle_add(self.show_err_msg, error)
                self.toolbarview.set_content(self.headapp)
                self.toolbarview.add_top_bar(self.headerbar)
                self.toolbarview.remove(self.headerbar_import)
            finally:
                if not e_o:
                    self.import_config()
                
        # action after closing dialog for checking password
        def checkDialog_closed(w, response):
            if response == 'ok':
                self.checkDialog.set_response_enabled("ok", False)
                zip_thread = Thread(target=unzip_ar)
                zip_thread.start()
            
        self.checkDialog = Adw.MessageDialog.new(self)
        self.checkDialog.set_heading(_["check_pwd_title"])
        self.checkDialog.set_body(_["check_pwd_desc"])
        
        self.checkEntry = Adw.PasswordEntryRow.new()
        self.checkEntry.set_title(_["password_entry"])
        self.checkDialog.set_extra_child(self.checkEntry)
        
        self.checkDialog.add_response("cancel", _["cancel"])
        self.checkDialog.add_response("ok", _["apply"])
        self.checkDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.checkDialog.connect('response', checkDialog_closed)
        self.checkDialog.show()    
        
    # Import configuration
    def import_config(self):
        if not os.path.exists(f"{CACHE}/import_config"):
            os.mkdir(f"{CACHE}/import_config")
        os.chdir(f"{CACHE}/import_config")
        import_thread = Thread(target=self.start_importing)
        import_thread.start()
       
    # start process of importing configuration
    def start_importing(self):
        try:
            e_o = False
            from config import Import
            Import()
        except Exception as e:
            e_o = True
            error = e
            GLib.idle_add(self.show_err_msg, error)
            self.toolbarview.set_content(self.headapp)
            self.toolbarview.remove(self.headerbar_import)
            self.toolbarview.add_top_bar(self.headerbar)
        finally:
            if not e_o:
                self.applying_done()
    
    # "Please wait" information on the "Import" page
    def please_wait_import(self):
        # Stop importing configuration
        def cancel_import(w):
            os.system(f"pkill -xf 'python3 {system_dir}/config.py --import_'")
            self.toolbarview.set_content(self.headapp)
            self.toolbarview.remove(self.headerbar_import)
            self.toolbarview.add_top_bar(self.headerbar)
            for widget in [self.importwaitSpinner, self.importwaitLabel, self.importwaitButton, self.idoneImage, self.logoutButton, self.backtomButton]:
                self.importwaitBox.remove(widget)

        # Get information about filename from this file
        with open(f'{CACHE}/.impfile.json') as i:
            config_name = json.load(i)["import_file"]

        # Add new headerbar for this page
        self.headerbar_import = Adw.HeaderBar.new()
        self.headerbar_import.pack_end(self.menu_button)
        self.toolbarview.add_top_bar(self.headerbar_import)

        # Remove main headerbar and headerbar for "Import from list" page
        try:
            self.toolbarview.remove(self.headerbar_list)
        except:
            self.toolbarview.remove(self.headerbar)

        # Create box widget for this page
        self.importwaitBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.importwaitBox.set_halign(Gtk.Align.CENTER)
        self.importwaitBox.set_valign(Gtk.Align.CENTER)
        self.toolbarview.set_content(self.importwaitBox)

        # Set bold title
        self.set_title(_["importing_config_status"].split('</b>')[0].split('<b>')[-1])

        # Create spinner for this page
        self.importwaitSpinner = Gtk.Spinner.new()
        self.importwaitSpinner.set_size_request(100, 100)
        self.importwaitSpinner.start()
        self.importwaitBox.append(self.importwaitSpinner)

        # Prepare Gtk.Image widget for this page
        self.idoneImage = Gtk.Image.new()
        self.importwaitBox.append(self.idoneImage)

        # Create label about configuration archive name
        self.importwaitLabel = Gtk.Label.new(str=_["importing_config_status"].format(config_name))
        self.importwaitLabel.set_use_markup(True)
        self.importwaitLabel.set_justify(Gtk.Justification.CENTER)
        self.importwaitLabel.set_wrap(True)
        self.importwaitBox.append(self.importwaitLabel)

        # Create button for canceling importing configuration
        self.importwaitButton = Gtk.Button.new_with_label(_["cancel"])
        self.importwaitButton.add_css_class("pill")
        self.importwaitButton.add_css_class("destructive-action")
        self.importwaitButton.connect("clicked", cancel_import)
        self.importwaitButton.set_margin_start(170)
        self.importwaitButton.set_margin_end(170)
        self.importwaitBox.append(self.importwaitButton)
    
    # Config has been imported action
    def applying_done(self):
        # back to the previous page from this page
        def back_to_main(w):
            self.toolbarview.set_content(self.headapp)
            self.toolbarview.remove(self.headerbar_import)
            self.toolbarview.add_top_bar(self.headerbar)
            [self.importwaitBox.remove(widget) for widget in [self.importwaitSpinner, self.importwaitLabel, self.importwaitButton, self.idoneImage, self.logoutButton, self.backtomButton]]
            self.headerbar.set_title_widget(self.switcher_title)
            if hasattr(self, 'flistBox'):
                self.pBox.remove(self.flistBox)
        
        # send notification about imported configuration if application window is inactive only
        self.notification_import = Gio.Notification.new("SaveDesktop")
        self.notification_import.set_body(_["config_imported"])
        active_window = app.get_active_window()
        if active_window is None or not active_window.is_active():
            app.send_notification(None, self.notification_import)
        
        # stop spinner animation
        self.importwaitSpinner.stop()
        self.importwaitBox.remove(self.importwaitButton)

        # set title to "Configuration has been applied!"
        self.set_title(_['config_imported'])

        # widget for showing done.svg icon
        self.idoneImage.set_from_icon_name("done")
        self.idoneImage.set_pixel_size(128)

        # edit label for the purposes of this page
        self.importwaitLabel.set_label(_["config_imported_desc"].format(_['config_imported']))

        # create button for loging out of the system
        self.logoutButton = Gtk.Button.new_with_label(_["logout"])
        self.logoutButton.add_css_class('pill')
        self.logoutButton.add_css_class('suggested-action')
        self.logoutButton.set_action_name('app.logout')
        self.logoutButton.set_margin_start(170)
        self.logoutButton.set_margin_end(170)
        self.importwaitBox.append(self.logoutButton)

        # create button for backing to the previous page
        self.backtomButton = Gtk.Button.new_with_label(_["back_to_page"])
        self.backtomButton.connect("clicked", back_to_main)
        self.backtomButton.add_css_class("pill")
        self.backtomButton.set_margin_start(170)
        self.backtomButton.set_margin_end(170)
        self.importwaitBox.append(self.backtomButton)
        
    # show message dialog in the error case
    def show_err_msg(self, error):
        self.errDialog = Adw.MessageDialog.new(app.get_active_window())
        self.errDialog.set_heading(heading="An error occured")
        self.errDialog.set_body(body=f"{error}")
        self.errDialog.add_response('cancel', _["cancel"])
        self.errDialog.show()
       
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
    
    # action after closing the main window
    def on_close(self, widget, *args):
        self.close()
        # Save window size, state, and filename
        settings["window-size"] = self.get_default_size()
        settings["maximized"] = self.is_maximized()
        settings["filename"] = self.saveEntry.get_text()
        
        # Check for ongoing operations before clearing cache
        if any(os.path.exists(f"{CACHE}/{path}") for path in [
            "import_config/copying_flatpak_data",
            "syncing/copying_flatpak_data",
            "periodic_saving/saving_status"
        ]):
            print("Flatpak data exists.")
        else:
            os.system(f"rm -rf {CACHE}/* {CACHE}/.*")
        
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE, 
                         application_id="io.github.vikdevelop.SaveDesktop" if not snap else None)
        self.create_action('about', self.on_about_action, ["F1"])
        self.create_action('open-dir', self.open_dir)
        self.create_action('logout', self.logout)
        self.create_action('m_sync_with_key', self.sync_pc, ["<primary>s"] if settings["manually-sync"] else None)
        self.create_action('quit', self.app_quit, ["<primary>q"])
        self.create_action('shortcuts', self.shortcuts, ["<primary>question"])
        self.connect('activate', self.on_activate)

    def open_dir(self, action, param):
        with open(f"{CACHE}/.filedialog.json") as fd:
            jf = json.load(fd)
        path = jf["recent_file"]
        Gtk.FileLauncher.new(Gio.File.new_for_path(path)).open_containing_folder()

    def logout(self, action, param):
        if snap:
            bus = dbus.SystemBus()
            manager = dbus.Interface(bus.get_object("org.freedesktop.login1", "/org/freedesktop/login1"), 'org.freedesktop.login1.Manager')
            manager.KillSession(manager.ListSessions()[0][0], 'all', 9)
        else:
            if os.getenv("XDG_CURRENT_DESKTOP") == 'XFCE':
                os.system("dbus-send --session --dest=org.xfce.SessionManager /org/xfce/SessionManager org.xfce.Session.Manager.Logout boolean:true boolean:false")
            elif os.getenv("XDG_CURRENT_DESKTOP") == 'KDE':
                os.system("dbus-send --dest=org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout int32:0 int32:0 int32:0")
            else:
                os.system("gdbus call --session --dest org.gnome.SessionManager --object-path /org/gnome/SessionManager --method org.gnome.SessionManager.Logout 1")

    def sync_pc(self, action, param):
        sync_info_path = f"{DATA}/sync-info.json"
        if os.path.exists(sync_info_path):
            os.remove(sync_info_path)
        os.system(f'notify-send "{_["please_wait"]}"')
        os.system(f"echo > {CACHE}/.from_app")
        self.sync_m = GLib.spawn_command_line_async(f"python3 {system_dir}/network_sharing.py")

    def shortcuts(self, action, param):
        ShortcutsWindow(transient_for=self.get_active_window()).present()

    def app_quit(self, action, param):
        if any(os.path.exists(f"{CACHE}/{path}") for path in [
            "import_config/copying_flatpak_data",
            "syncing/copying_flatpak_data",
            "periodic_saving/saving_status"
        ]):
            print("Flatpak data exists." if "import_config" in path else "Saving Flatpak apps data in progress")
        else:
            os.system(f"rm -rf {CACHE}/* {CACHE}/.*")
        app.quit()

    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("SaveDesktop")
        dialog.set_developer_name("vikdevelop")
        r_lang != "en" and dialog.set_translator_credits(_["translator_credits"]) # add the translator credits section if the system language is not English
        lang_list and dialog.add_link("SaveDesktop Github Wiki (Weblate)", "https://hosted.weblate.org/projects/vikdevelop/savedesktop-github-wiki/") # add a link to translate the SaveDesktop Github wiki on Weblate
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://github.com/vikdevelop/SaveDesktop")
        dialog.set_issue_url("https://github.com/vikdevelop/SaveDesktop/issues")
        dialog.set_copyright("© 2023-2024 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_artists(["Brage Fuglseth"])
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
