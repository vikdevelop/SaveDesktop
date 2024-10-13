#!/usr/bin/python3
import os, socket, glob, sys, shutil, re, zipfile, random, string, gi, warnings, tarfile
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk
from datetime import date
from pathlib import Path
from threading import Thread
from localization import _, home, download_dir, snap, flatpak
from open_wiki import *
from shortcuts_window import *
from items_dialog import FolderSwitchRow, FlatpakAppsDialog, itemsDialog

# Application window
class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("SaveDesktop")
        
        # header bar and toolbarview
        self.headerbar = Adw.HeaderBar.new()
        self.toolbarview = Adw.ToolbarView.new()
        self.toolbarview.add_top_bar(self.headerbar)
        
        # values that set if state of the switch "Extensions" in the Items, state of the switch "User data of installed Flatpak apps will be saved or not", if whether whether to reopen the self.setDialog and if the Apply button in self.setDialog will be enabled or not
        self.save_ext_switch_state = self.flatpak_data_sw_state = self.open_setdialog_tf = self.cancel_process = self.set_button_sensitive = False
        
        # set the window size and maximization from the GSettings database
        (width, height) = settings["window-size"]
        self.set_default_size(width, height)
        
        # if the value is TRUE, it enables window maximalization
        if settings["maximized"]:
            self.maximize()
        
        # App menu - primary menu
        self.main_menu = Gio.Menu()
        
        # primary menu section
        self.general_menu = Gio.Menu()
        self.general_menu.append(_["keyboard_shortcuts"], 'app.shortcuts')
        self.general_menu.append(_["about_app"], 'app.about')
        self.main_menu.append_section(None, self.general_menu)
        
        # menu button
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.main_menu)
        self.headerbar.pack_end(child=self.menu_button)
        
        # add Manually sync section
        if settings["manually-sync"] == True:
            self.sync_menu = Gio.Menu()
            self.sync_menu.append(_["sync"], 'app.m-sync-with-key')
            self.main_menu.prepend_section(None, self.sync_menu)
        
        # primary layout
        self.headapp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.headapp.set_valign(Gtk.Align.CENTER)
        self.headapp.set_halign(Gtk.Align.CENTER)
        self.toolbarview.set_content(self.headapp)
        
        # A view container for the menu switcher
        self.stack = Adw.ViewStack(vexpand=True)
        self.stack.set_hhomogeneous(True)
        self.headapp.append(self.stack)
        
        # Layout for saving and importing configuration
        self.saveBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.importBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.syncingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Add pages to the menu switcher
        self.stack.add_titled_with_icon(self.saveBox,"savepage",_["save"],"document-save-symbolic")
        self.stack.add_titled_with_icon(self.importBox,"importpage",_["import_title"],"document-open-symbolic")
        self.stack.add_titled_with_icon(self.syncingBox,"syncpage",_["sync"],"emblem-synchronizing-symbolic")
        
        # menu switcher
        self.switcher_title = Adw.ViewSwitcherTitle.new()
        self.switcher_title.set_stack(self.stack)
        self.switcher_title.set_title("SaveDesktop")
        self.headerbar.set_title_widget(self.switcher_title)
        self.switcher_title.connect("notify::title-visible", self.change_bar)
        
        # menu bar
        self.switcher_bar = Adw.ViewSwitcherBar.new()
        self.switcher_bar.set_stack(self.stack)
        self.toolbarview.add_bottom_bar(self.switcher_bar)
        
        # Toast Overlay for showing the popup window
        self.toast_overlay = Adw.ToastOverlay.new()
        self.toast_overlay.set_margin_top(margin=1)
        self.toast_overlay.set_margin_end(margin=1)
        self.toast_overlay.set_margin_bottom(margin=1)
        self.toast_overlay.set_margin_start(margin=1)
        self.toast_overlay.set_child(self.toolbarview)
        self.set_content(self.toast_overlay)
        
        # Popup window for showing messages about necessity to log out of the system after selected the periodic synchronization interval
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
            self.headerbar.set_title_widget(None)
            self.toolbarview.remove(self.switcher_bar)
            self.pBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.pBox.set_halign(Gtk.Align.CENTER)
            self.pBox.set_valign(Gtk.Align.CENTER)
            self.pBox.set_margin_start(50)
            self.pBox.set_margin_end(50)
            self.toolbarview.set_content(self.pBox)
            self.unsupp_img = Gtk.Image.new_from_icon_name("exclamation_mark"); self.unsupp_img.set_pixel_size(128); self.pBox.append(self.unsupp_img)
            self.unsupp_label = Gtk.Label.new(str=f'<big>{_["unsuppurted_env_desc"]}</big>'.format("GNOME, Xfce, Budgie, Cinnamon, COSMIC, Pantheon, KDE Plasma, MATE, Deepin")); self.unsupp_label.set_use_markup(True); self.unsupp_label.set_justify(Gtk.Justification.CENTER); self.unsupp_label.set_wrap(True); self.pBox.append(self.unsupp_label)
    
    # Switch between ViewSwitcherTitle and ViewSwitcherBar based on the title visible
    def change_bar(self, *data):
        if self.switcher_title.get_title_visible() == True:
            self.switcher_bar.set_reveal(True)
        else:
            self.switcher_bar.set_reveal(False)
    
    # Show main page
    def save_desktop(self):
        # More options dialog
        def more_options_dialog(w):
            # create desktop file for enabling periodic saving at startup
            def create_pb_desktop():
                if not os.path.exists(f'{home}/.config/autostart'):
                    os.mkdir(f'{home}/.config/autostart')
                if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh"):
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
                        w = ""
                        self.open_setDialog(w)

            # open a link to the wiki page about periodic saving
            def open_pb_wiki(w):
                os.system(f"xdg-open {pb_wiki}")

            # reset the file name format entry to the default value
            def reset_fileformat(w):
                self.filefrmtEntry.set_text("Latest_configuration")
            
            # Dialog for showing more options itself
            self.msDialog = Adw.AlertDialog.new()
            self.msDialog.set_heading(_["more_options"])
            self.msDialog.choose(self, None, None, None)

            # Box for this dialog
            self.msBox = Gtk.ListBox.new()
            self.msBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
            self.msBox.add_css_class('boxed-list')
            self.msBox.set_size_request(-1, 500) if self.open_setdialog_tf else self.msBox.set_size_request(-1, 300)
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
            self.saving_eRow.set_expanded(True) if self.open_setdialog_tf else None
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
            self.encryptRow.set_subtitle_lines(15)
            self.encryptRow.add_suffix(self.encryptSwitch)
            self.encryptRow.set_activatable_widget(self.encryptSwitch)
            self.msBox.append(self.encryptRow)

            # add response of this dialog
            self.msDialog.add_response('cancel', _["cancel"])
            self.msDialog.add_response('ok', _["apply"])
            self.msDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
            self.msDialog.connect('response', msDialog_closed)
            
            self.msDialog.present()
            
        def open_itemsDialog(w):
            self.itemsd = itemsDialog()
            self.itemsd.choose(self, None, None, None)
            self.itemsd.present()

        # =========
        # Save page
        
        # Open the More options dialog from the self.setDialog
        self.more_options_dialog = more_options_dialog
        self.items_dialog = open_itemsDialog
            
        # Set valign for save desktop layout
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
        self.lbox_e.add_css_class(css_class='boxed-list-separate')
        self.lbox_e.set_margin_start(20)
        self.lbox_e.set_margin_end(20)
        self.lbox_e.set_halign(Gtk.Align.CENTER)
        self.lbox_e.set_valign(Gtk.Align.CENTER)
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
        self.itemsButton.connect("clicked", open_itemsDialog)

        # Action row for opening dialog for selecting items that will be included to the config archive
        self.items_row = Adw.ActionRow.new()
        self.items_row.set_title(title=_["items_for_archive"])
        self.items_row.set_use_markup(True)
        self.items_row.set_title_lines(5)
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
        self.moreSettings.set_subtitle_lines(3)
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
        self.importBox.set_valign(Gtk.Align.CENTER)
        self.importBox.set_halign(Gtk.Align.CENTER)
        
        # Image and title for the Import page
        self.importPage = Adw.StatusPage.new()
        self.importPage.set_icon_name("document-open-symbolic")
        self.importPage.set_title(_['import_config'])
        self.importPage.set_description("Import the configuration by clicking on the button below.")
        self.importPage.set_size_request(300, 300)
        self.importBox.append(self.importPage)
        
        # Import configuration button
        self.fileButton = Gtk.Button.new_with_label(_["import_from_file"])
        self.fileButton.add_css_class("pill")
        self.fileButton.add_css_class("suggested-action")
        self.fileButton.set_halign(Gtk.Align.CENTER)
        self.fileButton.set_valign(Gtk.Align.CENTER)
        self.fileButton.connect("clicked", self.select_folder_to_import)
        self.importBox.append(self.fileButton)
            
    # Syncing desktop page
    def sync_desktop(self):
        self.syncingBox.set_valign(Gtk.Align.CENTER)
        self.syncingBox.set_halign(Gtk.Align.CENTER)

        # Image and title for this page
        self.syncPage = Adw.StatusPage.new()
        self.syncPage.set_icon_name("emblem-synchronizing-symbolic")
        self.syncPage.set_title(_["sync_title"])
        self.syncPage.set_description(f'{_["sync_desc"]} <a href="{sync_wiki}">{_["learn_more"]}</a>')
        self.syncPage.set_size_request(-1, 450)
        self.syncingBox.append(self.syncPage)

        # "Set up the sync file" button
        self.setButton = Gtk.Button.new_with_label(_["set_up_sync_file"])
        self.setButton.set_name("set-button")
        self.setButton.add_css_class("pill")
        self.setButton.add_css_class("suggested-action")
        self.setButton.connect("clicked", self.open_setDialog if not settings["first-synchronization-setup"] else self.open_initsetupDialog)
        self.setButton.set_valign(Gtk.Align.CENTER)
        self.setButton.set_halign(Gtk.Align.CENTER)
        self.syncingBox.append(self.setButton)

        # "Connect with other computer" button
        self.getButton = Gtk.Button.new_with_label(_["connect_cloud_storage"])
        self.getButton.set_name("get-button")
        self.getButton.add_css_class("pill")
        self.getButton.connect("clicked", self.open_cloudDialog if not settings["first-synchronization-setup"] else self.open_initsetupDialog)
        self.getButton.set_valign(Gtk.Align.CENTER)
        self.getButton.set_halign(Gtk.Align.CENTER)
        self.syncingBox.append(self.getButton)
    
    # Dialog for initial setting up the synchronization
    def open_initsetupDialog(self, w):
        # set the self.get_button_type variable before starting the dialog
        try:
            self.get_button_type = w.get_name()
        except AttributeError:
            self.get_button_type = w
        
        # show the message about finished setup the synchronization
        def almost_done():
            self.initsetupDialog.remove_response('ok-rclone')
            self.initsetupDialog.set_extra_child(None)
            self.initsetupDialog.remove_response('next')
            self.initsetupDialog.set_heading("Almost done!")
            self.initsetupDialog.set_body("You've now created the cloud folder! Click on the Next button to complete the setup.")
            self.initsetupDialog.set_can_close(True)
            self.initsetupDialog.add_response('open-setdialog', 'Next') if self.get_button_type == 'set-button' else self.initsetupDialog.add_response('open-clouddialog', 'Next')
            self.initsetupDialog.set_response_appearance('open-setdialog', Adw.ResponseAppearance.SUGGESTED) if self.get_button_type == 'set-button' else self.initsetupDialog.set_response_appearance('open-clouddialog', Adw.ResponseAppearance.SUGGESTED)
            
        # copy the command for setting up the Rclone using Gdk.Clipboard()
        def copy_rclone_command(w):
            clipboard = Gdk.Display.get_default().get_clipboard()
            Gdk.Clipboard.set(clipboard, f"rclone &> /dev/null && rclone config create drive {self.cloud_service} && rclone mount drive: {download_dir}/SaveDesktop/rclone_drive || echo 'Rclone is not installed. Please install it from this website first: https://rclone.org/install/.'")
            self.copyButton.set_icon_name("done")
            self.copyButton.set_tooltip_text("Copied to clipboard")
            
        # button for copying the command for setting up Rclone
        def copy_button():
            self.copyButton = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
            self.copyButton.add_css_class("circular")
            self.copyButton.set_valign(Gtk.Align.CENTER)
            self.copyButton.connect("clicked", copy_rclone_command)
            self.cmdRow.add_suffix(self.copyButton)
        
        # Set the Rclone setup command
        def get_service(comborow, GParamObject):
            self.initsetupDialog.set_body("")
            get_servrow = self.servRow.get_selected_item().get_string()
            self.cloud_service = "drive" if get_servrow == "Google Drive" else "onedrive" if get_servrow == "Microsoft OneDrive" else "dropbox"
            os.makedirs(f"{download_dir}/SaveDesktop/rclone_drive", exist_ok=True)
            self.cmdRow.set_title(f"Now, copy the command to setup Rclone using the side button and open the terminal app using Ctrl+Alt+T keyboard shortcut or finding it in the apps menu.")
            copy_button()
            self.initsetupDialog.set_response_enabled('ok-rclone', True)
            
        # Responses of this dialog
        def initsetupDialog_closed(w, response):
            if response == 'next': # open the Gtk.FileDialog in the GNOME Online accounts case
                self.select_pb_folder(w) if self.get_button_type == 'set-button' else self.select_sync_folder(w)
                almost_done()
            elif response == 'ok-rclone': # set the periodic saving folder in the Rclone case
                settings["periodic-saving-folder"] = f"{download_dir}/SaveDesktop/rclone_drive"
                almost_done()
            elif response == 'cancel': # if the user clicks on the Cancel button
                self.initsetupDialog.set_can_close(True)
            elif response == 'open-setdialog': # open the "Set up the sync file" dialog after clicking on the Next button in "Almost done!" page
                self.start_saving = True
                settings["periodic-saving"] = "Daily"
                settings["first-synchronization-setup"] = False
                self.open_setDialog(w)
            elif response == 'open-clouddialog': # open the "Connect to the cloud folder" dialog after clicking on the Next button in "Almost done!" page
                self.open_cloudDialog(w)
                settings["first-synchronization-setup"] = False
        
        # Dialog itself
        self.initsetupDialog = Adw.AlertDialog.new()
        self.initsetupDialog.set_heading("Initial synchronization setup")
        self.initsetupDialog.choose(self, None, None, None)
        self.initsetupDialog.set_body_use_markup(True)
        self.initsetupDialog.set_can_close(False)
        self.initsetupDialog.add_response('cancel', _["cancel"])
        self.initsetupDialog.connect('response', initsetupDialog_closed)
        self.initsetupDialog.present()
        
        # if the user has GNOME, Cinnamon, COSMIC (Old) or Budgie environment, it shows text about setting up GNOME Online Accounts.
        # otherwise, it shows the text about setting up Rclone
        if self.environment in ["GNOME", "Cinnamon", "COSMIC (Old)", "Budgie"]:
            self.initsetupDialog.set_body("For synchronization to works properly, you need to have the folder, that is synced with your cloud service using GNOME Online Accounts.\nTo setup it, <b>go to the system settings and then to the Online Accounts section and select the service you want</b> (e.g., Google, Microsoft 365, Nextcloud).\n<b>Then, click on the Next button and select the created cloud folder, which can be found in the Other locations > Networks.</b>")
            self.initsetupDialog.add_response('next', 'Next')
            self.initsetupDialog.set_response_appearance('next', Adw.ResponseAppearance.SUGGESTED)
        else:
            self.initsetupDialog.set_body("For synchronization to works properly, you need to have the folder, that is synced with your cloud service using Rclone.\n<b>Start by selecting the cloud drive service you use.</b>")
            
            # create a list with available services, which can be connected via Rclone
            services = Gtk.StringList.new(strings=['Select', 'Google Drive', 'Microsoft OneDrive', 'DropBox'])
            
            # create a ListBox for the combo row below
            self.initBox = Gtk.ListBox.new()
            self.initBox.set_selection_mode(Gtk.SelectionMode.NONE)
            self.initBox.get_style_context().add_class('boxed-list')
            self.initsetupDialog.set_extra_child(self.initBox)
            
            # row for selecting the cloud service
            self.servRow = Adw.ComboRow.new()
            self.servRow.set_model(services)
            self.servRow.connect("notify::selected-item", get_service)
            self.initBox.append(self.servRow)
            
            # row for showing the command for setting up the Rclone
            self.cmdRow = Adw.ActionRow.new()
            self.cmdRow.set_title_selectable(True)
            self.cmdRow.set_use_markup(True)
            self.initBox.append(self.cmdRow)
            
            # add the Apply button to the dialog
            self.initsetupDialog.add_response('ok-rclone', _["apply"])
            self.initsetupDialog.set_response_appearance('ok-rclone', Adw.ResponseAppearance.SUGGESTED)
            self.initsetupDialog.set_response_enabled('ok-rclone', False)
    
    # Dialog for setting the sync file, periodic synchronization interval and copying the URL for synchronization
    def open_setDialog(self, w):
        # Create periodic saving file if it does not exist
        def save_now():
            try:
                e_o = False
                subprocess.run(['notify-send', 'SaveDesktop', _["please_wait"]])
                self.file_row.set_subtitle(_["please_wait"])
                self.file_row.set_use_markup(False)
                from periodic_saving import PeriodicBackups
                pb = PeriodicBackups()
                pb.run(now=True)
            except Exception as e:
                e_o = True
                subprocess.run(['notify-send', _["err_occured"], f'{e}'])
                self.file_row.set_subtitle(f'{e}')
            finally:
                if not e_o:
                    self.file_row.remove(self.setupButton)
                    self.file_row.set_subtitle(f'{settings["periodic-saving-folder"]}/{settings["filename-format"]}.sd.tar.gz')
                    os.system(f"notify-send 'SaveDesktop' '{_['config_saved']}'")
                    self.setDialog.set_response_enabled('ok', True)
        
        # make the periodic saving file if it does not exist
        def make_pb_file(w):
            self.setupButton.set_sensitive(False)
            pb_thread = Thread(target=save_now)
            pb_thread.start()
            
        # Refer to the article about synchronization
        def open_sync_link(w):
            os.system(f"xdg-open {sync_wiki}")
        
        def update_gui():
            global folder, path, check_filesystem
            self.file_row = Adw.ActionRow()
            self.file_row.set_title(_["periodic_saving_file"])
            self.file_row.set_subtitle(folder)
            if "fuse" in check_filesystem and "red" not in folder:
                self.file_row.add_suffix(Gtk.Image.new_from_icon_name("network-wired-symbolic"))
            self.file_row.set_subtitle_lines(4)
            self.file_row.set_use_markup(True)
            self.file_row.set_subtitle_selectable(True)
            self.l_setdBox.append(self.file_row)
            self.l_setdBox.append(self.ps_row)
            
            set_button_sensitive = settings["periodic-saving"] != "Never" and not os.path.exists(path)
            if "red" in folder:
                self.setDialog.set_response_enabled('ok', False)
            if _["periodic_saving_file_err"] in folder:
                self.setupButton = Gtk.Button.new_with_label(_["create"])
                self.setupButton.set_valign(Gtk.Align.CENTER)
                self.setupButton.add_css_class("suggested-action")
                self.setupButton.connect("clicked", make_pb_file)
                self.file_row.add_suffix(self.setupButton)
                make_pb_file(w) if self.start_saving else None
            if _["cloud_folder_err"] in folder:
                self.lmButton = Gtk.Button.new_with_label(_["learn_more"])
                self.lmButton.set_valign(Gtk.Align.CENTER)
                self.lmButton.add_css_class("suggested-action")
                self.lmButton.connect("clicked", open_sync_link)
                self.file_row.add_suffix(self.lmButton)
        
        # Check the file system of the periodic saving folder and their existation
        def check_filesystem_fnc():
            global folder, path, check_filesystem
            check_filesystem = subprocess.getoutput('df -T "%s" | awk \'NR==2 {print $2}\'' % settings["periodic-saving-folder"] if not snap else subprocess.getoutput('stat -f "%s"' % settings["periodic-saving-folder"]))
            
            path = f'{settings["periodic-saving-folder"]}/{settings["filename-format"].replace(" ", "_")}.sd.tar.gz'
            
            # Check if periodic saving is set to "Never"
            if settings["periodic-saving"] == "Never":
                folder = f'<span color="red">{_["pb_interval"]}: {_["never"]}</span>'
            # Check if the filesystem is not FUSE
            elif (not snap and (not "gvfs" in check_filesystem or not "rclone" in check_filesystem)) or (snap and not "fuse" in check_filesystem):
                folder = f'<span color="red">{_["cloud_folder_err"]}</span>'
            # Check if the periodic saving file exists
            elif not os.path.exists(path):
                folder = f'<span color="red">{_["periodic_saving_file_err"]}</span>'
            else:
                folder = path
            
            update_gui()
        
        # save the SaveDesktop.json file to the periodic saving folder and set up the auto-mounting the cloud drive
        def save_file():
            open(f"{settings['periodic-saving-folder']}/SaveDesktop.json", "w").write('{\n "periodic-saving-interval": "%s",\n "filename": "%s"\n}' % (settings["periodic-saving"], settings["filename-format"]))
            self.set_up_auto_mount()
        
        # Action after closing dialog for setting synchronization file
        def setDialog_closed(w, response):
            if response == 'ok':
                self.open_setdialog_tf = False
                
                thread = Thread(target=save_file)
                thread.start()
            else:
                self.open_setdialog_tf = False
        
        # Dialog itself
        self.setDialog = Adw.AlertDialog.new()
        self.setDialog.set_heading(_["set_up_sync_file"])
        self.setDialog.set_body_use_markup(True)
        self.setDialog.choose(self, None, None, None)
        
        # List Box for appending widgets
        self.l_setdBox = Gtk.ListBox.new()
        self.l_setdBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.l_setdBox.get_style_context().add_class('boxed-list')
        self.l_setdBox.set_size_request(-1, 160)
        self.setDialog.set_extra_child(self.l_setdBox)
        
        # Check the synchronization matters
        check_thread = Thread(target=check_filesystem_fnc)
        check_thread.start()
        
        # Button for opening More options dialog
        self.open_setdialog_tf = True
        self.ps_button = Gtk.Button.new_with_label(_["change"])
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

        # Dialog responses
        self.setDialog.add_response('cancel', _["cancel"])
        self.setDialog.add_response('ok', _["apply"])
        self.setDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.setDialog.connect('response', setDialog_closed)
        self.setDialog.present()
    
    # Dialog for selecting the cloud drive folder and periodic synchronization interval
    def open_cloudDialog(self, w):
        # reset the cloud folder selection to the default value
        def reset_cloud_folder(w):
            self.cfileRow.set_subtitle("")
            self.cfileRow.remove(self.resetButton)
            self.cloudDialog.set_response_enabled('ok', True)
            settings["file-for-syncing"] = self.cfileRow.get_subtitle()
            [os.remove(path) for path in [f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.sync.desktop", f"{DATA}/savedesktop-synchronization.sh"] if os.path.exists(path)]
            
        # enable or disable the response of this dialog in depending on the selected periodic synchronization interval
        def on_psync_changed(psyncRow, GParamObject):
            self.cloudDialog.set_response_enabled('ok', True) if not self.psyncRow.get_selected_item().get_string() == _["never"] else self.cloudDialog.set_response_enabled('ok', False)
        
        # Action after closing URL dialog
        def cloudDialog_closed(w, response):
            if response == 'ok':
                check_psync = settings["periodic-import"]
                
                # translate the periodic sync options to English
                selected_item = self.psyncRow.get_selected_item()
                sync = {_["never"]: "Never2", _["manually"]: "Manually2", _["daily"]: "Daily2", _["weekly"]: "Weekly2", _["monthly"]: "Monthly2"}
                
                sync_item = sync.get(selected_item.get_string(), "Never2")

                settings["periodic-import"] = sync_item
                
                # if the selected periodic saving interval is "Manually2", it enables the manually-sync value
                settings["manually-sync"] = True and settings["periodic-import"] == "Manually2"
                
                # save the status of the Bidirectional Synchronization switch
                settings["bidirectional-sync"] = self.bsSwitch.get_active()
                
                check_filesystem = subprocess.getoutput('df -T "%s" | awk \'NR==2 {print $2}\'' % self.cfileRow.get_subtitle()) if not snap else subprocess.getoutput('stat -f "%s"' % self.cfileRow.get_subtitle())
                
                if self.cfileRow.get_subtitle():
                    # Check if the selected cloud drive folder is correct
                    if (not snap and ("gvfs" in check_filesystem or "rclone" in check_filesystem)) or (snap and "fuse" in check_filesystem):
                        settings["file-for-syncing"] = self.cfileRow.get_subtitle()
                        
                        # if it is selected to manually sync, it creates an option in the app menu in the header bar
                        if settings["manually-sync"]:
                            self.sync_menu = Gio.Menu()
                            self.sync_menu.append(_["sync"], 'app.m-sync-with-key')
                            self.main_menu.prepend_section(None, self.sync_menu)
                            self.show_special_toast()
                        else:
                            try:
                                self.sync_menu.remove_all()
                            except:
                                pass

                            self.set_up_auto_mount()
                            
                        # check if the selected periodic sync interval was Never: if yes, shows the message about the necessity to log out of the system
                        if check_psync == "Never2":
                            if not settings["periodic-import"] == "Never2":
                                self.show_warn_toast()
                    else:
                        os.system(f"notify-send \"{_['err_occured']}\" \"{_['cloud_folder_err']}\"")
                        settings["file-for-syncing"] = ""
                else:
                    pass

        # Dialog itself
        self.cloudDialog = Adw.AlertDialog.new()
        self.cloudDialog.set_heading(_["connect_cloud_storage"])
        self.cloudDialog.set_body(_["connect_cloud_storage_desc"])
        self.cloudDialog.choose(self, None, None, None)
          
        # Box for adding widgets in this dialog
        self.cloudBox = Gtk.ListBox.new()
        self.cloudBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.cloudBox.get_style_context().add_class(class_name='boxed-list')
        self.cloudBox.set_size_request(-1, 400)
        self.cloudDialog.set_extra_child(self.cloudBox)
        
        # Row and buttons for selecting the cloud drive folder
        ## button for selecting the cloud drive folder
        self.cloudButton = Gtk.Button.new_from_icon_name("document-open-symbolic")
        self.cloudButton.add_css_class('flat')
        self.cloudButton.set_valign(Gtk.Align.CENTER)
        self.cloudButton.set_tooltip_text(_["set_another"])
        self.cloudButton.connect("clicked", self.select_sync_folder)
        
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
        self.cfileRow.set_title(_["select_cloud_folder_btn"])
        self.cfileRow.set_subtitle(settings["file-for-syncing"])
        self.cfileRow.set_subtitle_selectable(True)
        self.cfileRow.add_suffix(self.cloudButton)
        self.cfileRow.set_activatable_widget(self.cloudButton)
        self.cloudBox.append(self.cfileRow)
        
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
        self.psyncRow.connect('notify::selected-item', on_psync_changed)
        self.cloudBox.append(self.psyncRow)

        # Load periodic sync values form GSettings database
        old_psync = settings["periodic-import"]
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
            
        # Bidirectional Synchronization section
        ## Switch
        self.bsSwitch = Gtk.Switch.new()
        if settings["bidirectional-sync"] == True:
            self.bsSwitch.set_active(True)
        self.bsSwitch.set_valign(Gtk.Align.CENTER)
        
        ## Action Row
        self.bsyncRow = Adw.ActionRow.new()
        self.bsyncRow.set_title(_["bidirectional_sync"])
        self.bsyncRow.set_subtitle(_["bidirectional_sync_desc"])
        self.bsyncRow.set_title_lines(2)
        self.bsyncRow.add_suffix(self.bsSwitch)
        self.bsyncRow.set_activatable_widget(self.bsSwitch)
        self.cloudBox.append(self.bsyncRow)
        
        self.cloudDialog.add_response('cancel', _["cancel"])
        self.cloudDialog.add_response('ok', _["apply"])
        self.cloudDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        if not self.cfileRow.get_subtitle():
            self.cloudDialog.set_response_enabled('ok', False)
        else:
            self.cloudDialog.set_response_enabled('ok', True)
        self.cloudDialog.connect('response', cloudDialog_closed)
        self.cloudDialog.present()
      
    # set up auto-mounting of the cloud drives after logging in to the system
    def set_up_auto_mount(self):
        if not settings["periodic-saving-folder"] == "":
            cfile_subtitle = settings["periodic-saving-folder"]
        elif not self.cfileRow.get_subtitle() == "":
            cfile_subtitle = self.cfileRow.get_subtitle()
        else:
            cfile_subtitle = ""
        
        if cfile_subtitle:
            if settings["periodic-import"] != "Manually2" and "gvfs" in cfile_subtitle:
                pattern = r'.*/gvfs/([^:]*):host=([^,]*),user=([^/]*).*' if "onedrive" not in cfile_subtitle else r'.*/gvfs/([^:]*):host=([^/]*).*'
                match = re.search(pattern, cfile_subtitle)

                if match:
                    cloud_service = match.group(1)
                    host = match.group(2)
                    user = match.group(3) if "onedrive" not in cfile_subtitle else None
                    
                    cmd = f"gio mount {cloud_service}://{user}@{host}" if not "onedrive" in cfile_subtitle else f"gio mount {cloud_service}://{host}"
                else:
                    print("Failed to extract the necessary values to set up automatic cloud storage connection after logging into the system.")
            else:
                cmd = f"rclone mount {cfile_subtitle.split('/')[-1]}: {cfile_subtitle.split('/')[-1]}"
            synchronization_content = f'#!/usr/bin/bash\n{cmd}\n{periodic_saving_cmd}\n{sync_cmd}\n'
            if flatpak:
                synchronization_content += 'python3 ~/.var/app/io.github.vikdevelop.SaveDesktop/data/install_flatpak_from_script.py'
            with open(f"{DATA}/savedesktop-synchronization.sh", "w") as f:
                f.write(synchronization_content)
            open(f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.sync.desktop", "w").write(f"[Desktop Entry]\nName=SaveDesktop (Synchronization)\nType=Application\nExec=sh {DATA}/savedesktop-synchronization.sh")
            [os.remove(path) for path in [f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.MountDrive.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.server.desktop", f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Flatpak.desktop"] if os.path.exists(path)]
    
    # Select folder for periodic backups (Gtk.FileDialog)
    def select_pb_folder(self, w):
        def save_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except:
                return
            self.folder_pb = folder.get_path()
            self.dirRow.set_subtitle(self.folder_pb)
            settings["periodic-saving-folder"] = self.folder_pb if settings["first-synchronization-setup"] else None
        
        self.pb_chooser = Gtk.FileDialog.new()
        self.pb_chooser.set_modal(True)
        self.pb_chooser.set_title(_["set_pb_folder_tooltip"])
        self.pb_chooser.select_folder(self, None, save_selected, None)
    
    # Select folder for saving configuration
    def select_folder(self, w):
        def save_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except:
                return
            self.folder = folder.get_path()
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
                
        self.cancel_process = False # set this value to False before saving the configuration, as it may already be set to True due to the recent cancellation of the configuration save
        
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
            self.import_file = file.get_path()
            if ".sd.zip" in self.import_file:
                self.check_password_dialog()
            else:
                self.import_config()
                
        self.cancel_process = False # set this value to False before importing the configuration, as it may already be set to True due to the recent cancellation of the configuration import
        
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
    def select_sync_folder(self, w):
        def set_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except:
                return
            self.sync_folder = folder.get_path()
            self.cfileRow.set_subtitle(self.sync_folder)
            self.cloudDialog.set_response_enabled('ok', True) if not self.psyncRow.get_selected_item().get_string() == _["never"] else None
            settings["file-for-syncing"] = self.sync_folder if settings["first-synchronization-setup"] else None
            
        self.sync_folder_chooser = Gtk.FileDialog.new()
        self.sync_folder_chooser.set_modal(True)
        self.sync_folder_chooser.set_title(_["select_cloud_folder_btn"])
        self.sync_folder_chooser.select_folder(self, None, set_selected, None)
        
    # Dialog for creating password for the config archive
    def create_password_dialog(self):
        # Action after closing pswdDialog
        def pswdDialog_closed(w, response):
            if response == 'ok':
                self.password = self.pswdEntry.get_text()
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
        self.pswdDialog = Adw.AlertDialog.new()
        self.pswdDialog.set_heading(_["create_pwd_title"])
        self.pswdDialog.set_body(_["create_pwd_desc"])
        self.pswdDialog.choose(self, None, None, None)

        # button for generating strong password
        self.pswdgenButton = Gtk.Button.new_from_icon_name("emblem-synchronizing-symbolic")
        self.pswdgenButton.set_tooltip_text(_["gen_password"])
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
        self.pswdDialog.present()
    
    # Save configuration
    def save_config(self):
        self.please_wait_save()
        os.makedirs(f"{CACHE}/save_config", exist_ok=True)
        os.chdir(f"{CACHE}/save_config")
        save_thread = Thread(target=self.start_saving)
        save_thread.start()
        
    # start process of saving the configuration
    def start_saving(self):
        try:
            e_o = False
            os.system(f"python3 {system_dir}/config.py --save")
            if settings["enable-encryption"] == True:
                os.system(f"zip -9 -P '{self.password}' cfg.sd.zip . -r -x 'saving_status'")
                if self.cancel_process:
                    return
                else:
                    shutil.copyfile('cfg.sd.zip', f"{self.folder}/{self.filename_text}.sd.zip")
            else:
                os.system(f"tar --exclude='cfg.sd.tar.gz' --gzip -cf cfg.sd.tar.gz ./")
                if self.cancel_process:
                    return
                else:
                    shutil.copyfile('cfg.sd.tar.gz', f"{self.folder}/{self.filename_text}.sd.tar.gz")
            print("Configuration saved successfully.")
        except Exception as e:
            e_o = True
            error = e
            GLib.idle_add(self.show_err_msg, error) if not self.cancel_process else None
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
            self.cancel_process = True
            os.system(f"pkill -xf 'python3 {system_dir}/config.py --save'")
            os.system(f"pkill tar") if not settings["enable-encryption"] else os.system("pkill zip")
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(True)
            self.set_title("SaveDesktop")
            for widget in [self.savewaitSpinner, self.savewaitLabel, self.savewaitButton, self.sdoneImage, self.opensaveButton, self.backtomButton]:
                self.savewaitBox.remove(widget)
        
        self.headerbar.set_title_widget(None)
        self.switcher_bar.set_reveal(False)

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
        self.savewaitButton.set_valign(Gtk.Align.CENTER)
        self.savewaitButton.set_halign(Gtk.Align.CENTER)
        self.savewaitBox.append(self.savewaitButton)
        
    # config has been saved action
    def exporting_done(self):
        # back to the previous page from this page
        def back_to_main(w):
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(True)
            self.set_title("SaveDesktop")
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
        self.opensaveButton.set_action_name("app.open_dir")
        self.opensaveButton.set_valign(Gtk.Align.CENTER)
        self.opensaveButton.set_halign(Gtk.Align.CENTER)
        self.savewaitBox.append(self.opensaveButton)

        # create button for backing to the previous page
        self.backtomButton = Gtk.Button.new_with_label(_["back_to_page"])
        self.backtomButton.connect("clicked", back_to_main)
        self.backtomButton.add_css_class("pill")
        self.backtomButton.set_valign(Gtk.Align.CENTER)
        self.backtomButton.set_halign(Gtk.Align.CENTER)
        self.savewaitBox.append(self.backtomButton)
        
        # remove content in the cache directory
        os.popen(f"rm -rf {CACHE}/save_config/")
     
    # dialog for entering password of the archive
    def check_password_dialog(self):     
        # action after closing dialog for checking password
        def checkDialog_closed(w, response):
            if response == 'ok':
                self.checkDialog.set_response_enabled("ok", False)
                self.import_config()
            
        self.checkDialog = Adw.AlertDialog.new()
        self.checkDialog.set_heading(_["check_pwd_title"])
        self.checkDialog.set_body(_["check_pwd_desc"])
        self.checkDialog.choose(self, None, None, None)
        
        self.checkEntry = Adw.PasswordEntryRow.new()
        self.checkEntry.set_title(_["password_entry"])
        self.checkDialog.set_extra_child(self.checkEntry)
        
        self.checkDialog.add_response("cancel", _["cancel"])
        self.checkDialog.add_response("ok", _["apply"])
        self.checkDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.checkDialog.connect('response', checkDialog_closed)
        self.checkDialog.present()
        
    # Import configuration
    def import_config(self):
        self.please_wait_import()
        os.makedirs(f"{CACHE}/import_config", exist_ok=True)
        os.chdir(f"{CACHE}/import_config")
        import_thread = Thread(target=self.start_importing)
        import_thread.start()
       
    # start process of importing configuration
    def start_importing(self):
        try:
            e_o = False
            os.system("echo > import_status")
            if ".sd.zip" in self.import_file:
                with zipfile.ZipFile(self.import_file, "r") as zip_ar:
                    for member in zip_ar.namelist():
                        if self.cancel_process:
                            return
                        zip_ar.extract(member, path=f"{CACHE}/import_config", pwd=self.checkEntry.get_text().encode("utf-8"))
            else:
                with tarfile.open(self.import_file, 'r:gz') as tar:
                    for member in tar.getmembers():
                        try:
                            if self.cancel_process:
                                return
                            tar.extract(member, path=f"{CACHE}/import_config")
                        except PermissionError as e:
                            print(f"Permission denied for {member.name}: {e}")
            os.system(f"python3 {system_dir}/config.py --import_")
            os.system("rm import_status") if not os.path.exists(f"{CACHE}/import_config/app") else None
            print("Configuration imported successfully.")
        except Exception as e:
            e_o = True
            error = e
            GLib.idle_add(self.show_err_msg, error) if not self.cancel_process else None
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
            self.cancel_process = True
            os.system(f"pkill -xf 'python3 {system_dir}/config.py --import_'")
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(True)
            self.set_title("SaveDesktop")
            for widget in [self.importwaitSpinner, self.importwaitLabel, self.importwaitButton, self.idoneImage, self.logoutButton, self.backtomButton]:
                self.importwaitBox.remove(widget)

        # Add new headerbar for this page
        self.headerbar.set_title_widget(None)
        self.switcher_bar.set_reveal(False)

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
        self.importwaitLabel = Gtk.Label.new(str=_["importing_config_status"].format(self.import_file))
        self.importwaitLabel.set_use_markup(True)
        self.importwaitLabel.set_justify(Gtk.Justification.CENTER)
        self.importwaitLabel.set_wrap(True)
        self.importwaitBox.append(self.importwaitLabel)

        # Create button for canceling importing configuration
        self.importwaitButton = Gtk.Button.new_with_label(_["cancel"])
        self.importwaitButton.add_css_class("pill")
        self.importwaitButton.add_css_class("destructive-action")
        self.importwaitButton.connect("clicked", cancel_import)
        self.importwaitButton.set_halign(Gtk.Align.CENTER)
        self.importwaitButton.set_valign(Gtk.Align.CENTER)
        self.importwaitBox.append(self.importwaitButton)
    
    # Config has been imported action
    def applying_done(self):
        # back to the previous page from this page
        def back_to_main(w):
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(True)
            self.set_title("SaveDesktop")
            [self.importwaitBox.remove(widget) for widget in [self.importwaitSpinner, self.importwaitLabel, self.importwaitButton, self.idoneImage, self.logoutButton, self.backtomButton]]
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
        self.logoutButton.set_halign(Gtk.Align.CENTER)
        self.logoutButton.set_valign(Gtk.Align.CENTER)
        self.logoutButton.set_action_name("app.logout")
        self.importwaitBox.append(self.logoutButton)

        # create button for backing to the previous page
        self.backtomButton = Gtk.Button.new_with_label(_["back_to_page"])
        self.backtomButton.connect("clicked", back_to_main)
        self.backtomButton.add_css_class("pill")
        self.backtomButton.set_halign(Gtk.Align.CENTER)
        self.backtomButton.set_valign(Gtk.Align.CENTER)
        self.importwaitBox.append(self.backtomButton)
        
    # show message dialog in the error case
    def show_err_msg(self, error):
        self.errDialog = Adw.AlertDialog.new()
        self.errDialog.choose(self, None, None, None)
        self.errDialog.set_heading(heading=_["err_occured"])
        self.errDialog.set_body(body=f"{error}")
        self.errDialog.add_response('cancel', _["cancel"])
        self.errDialog.present()
       
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
    def on_close(self, w):
        self.close()
        # Save window size, state, and filename
        settings["window-size"] = self.get_default_size()
        settings["maximized"] = self.is_maximized()
        settings["filename"] = self.saveEntry.get_text()
        
        # Check for ongoing operations before clearing cache
        if any(os.path.exists(f"{CACHE}/{path}") for path in ["import_config/import_status", "syncing/sync_status""periodic_saving/saving_status"]):
            print("saving/importing/syncing configuration in progress...")
        else:
            os.popen(f"rm -rf {CACHE}/* {CACHE}/.*")

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE,
                         application_id="io.github.vikdevelop.SaveDesktop" if not snap else None)
        self.create_action('m-sync-with-key', self.sync_pc, ["<primary>m"] if settings["manually-sync"] else None)
        self.create_action('save-config', self.call_saving_config, ["<primary>s"])
        self.create_action('import-config', self.call_importing_config, ["<primary>i"])
        self.create_action('ms-dialog', self.call_ms_dialog, ["<primary><shift>m"])
        self.create_action('items-dialog', self.call_items_dialog, ["<primary><shift>i"])
        self.create_action('set-dialog', self.call_setDialog, ["<primary><shift>s"])
        self.create_action('cloud-dialog', self.call_cloudDialog, ["<primary><shift>c"])
        self.create_action('open-wiki', self.open_wiki, ["F1"])
        self.create_action('quit', self.app_quit, ["<primary>q"])
        self.create_action('shortcuts', self.shortcuts, ["<primary>question"])
        self.create_action('logout', self.logout)
        self.create_action('open_dir', self.open_dir)
        self.create_action('about', self.on_about_action)
        self.connect('activate', self.on_activate)
    
    # Synchronize configuation manually after clicking on the "Sync" button in the header bar menu
    def sync_pc(self, action, param):
        os.system(f'notify-send "{_["please_wait"]}"')
        os.system(f"echo > {CACHE}/.from_app")
        self.sync_m = GLib.spawn_command_line_async(f"python3 {system_dir}/network_sharing.py")
    
    # Start saving the configuration using Ctrl+S keyboard shortcut
    def call_saving_config(self, action, param):
        w = ""
        self.win.select_folder(w)
    
    # Start importing the configuration using Ctrl+I keyboard shortcut
    def call_importing_config(self, action, param):
        w = ""
        self.win.select_folder_to_import(w)
    
    # Open the More options dialog using Ctrl+Shift+M keyboard shortcut
    def call_ms_dialog(self, action, param):
        w = ""
        self.win.more_options_dialog(w)
        self.win.msDialog.present()
        
    # Open the "Items to include in the configuration archive" dialog using Ctrl+Shift+I keyboard shortcut
    def call_items_dialog(self, action, param):
        w = ""
        self.win.items_dialog(w)
    
    # Open the "Set up the sync file" dialog using Ctrl+Shift+S keyboard shortcut
    def call_setDialog(self, action, param):
        w = "set-button"
        self.win.open_setDialog(w) if not settings["first-synchronization-setup"] else self.win.open_initsetupDialog(w)
        
    # Open the "Connect to the cloud drive" dialog using Ctrl+Shift+C keyboard shortcut
    def call_cloudDialog(self, action, param):
        w = "get-button"
        self.win.open_cloudDialog(w) if not settings["first-synchronization-setup"] else self.win.open_initsetupDialog(w)
    
    # Open the application wiki using F1 keyboard shortcut
    def open_wiki(self, action, param):
        os.system("xdg-open https://vikdevelop.github.io/SaveDesktop/wiki")
    
    # Action after closing the application using Ctrl+Q keyboard shortcut
    def app_quit(self, action, param):
        w = ""
        self.win.on_close(w)
        self.quit()
    
    # Show Keyboard Shortcuts window
    def shortcuts(self, action, param):
        ShortcutsWindow(transient_for=self.get_active_window()).present()
        
    # log out of the system after clicking on the "Log Out" button
    def logout(self, action, param):
        if snap:
            bus = dbus.SystemBus()
            manager = dbus.Interface(bus.get_object("org.freedesktop.login1", "/org/freedesktop/login1"), 'org.freedesktop.login1.Manager')
            manager.KillSession(manager.ListSessions()[0][0], 'all', 9)
        else:
            if self.win.environment == 'Xfce':
                os.system("dbus-send --print-reply --session --dest=org.xfce.SessionManager /org/xfce/SessionManager org.xfce.Session.Manager.Logout boolean:true boolean:false")
            elif self.win.environment == 'KDE Plasma':
                os.system("dbus-send --print-reply --session --dest=org.kde.LogoutPrompt /LogoutPrompt org.kde.LogoutPrompt.promptLogout")
            elif self.win.environment == 'COSMIC (New)':
                os.system("dbus-send --print-reply --session --dest=com.system76.CosmicSession --type=method_call /com/system76/CosmicSession com.system76.CosmicSession.Exit")
            else:
                os.system("gdbus call --session --dest org.gnome.SessionManager --object-path /org/gnome/SessionManager --method org.gnome.SessionManager.Logout 1")
    
    # open directory with created configuration archive after clicking on the "Open the folder" button
    def open_dir(self, action, param):
        Gtk.FileLauncher.new(Gio.File.new_for_path(f"{self.win.folder}/{self.win.filename_text}.sd.tar.gz" if not settings["enable-encryption"] else f"{self.win.folder}/{self.win.filename_text}.sd.zip")).open_containing_folder()
    
    # "About app" dialog
    def on_about_action(self, action, param):
        dialog = Adw.AboutDialog()
        dialog.set_application_name("SaveDesktop")
        dialog.set_developer_name("vikdevelop")
        r_lang != "en" and dialog.set_translator_credits(_["translator_credits"]) # add the translator credits section if the system language is not English
        lang_list and dialog.add_link("SaveDesktop Github Wiki (Weblate)", "https://hosted.weblate.org/projects/vikdevelop/savedesktop-github-wiki/") # add a link to translate the SaveDesktop Github wiki on Weblate
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_website("https://vikdevelop.github.io/SaveDesktop")
        dialog.set_issue_url("https://github.com/vikdevelop/SaveDesktop/issues")
        dialog.add_link("Flathub Beta", "https://github.com/vikdevelop/savedesktop?tab=readme-ov-file#1-flathub-beta") if flatpak else dialog.add_link("Snap Beta", "https://github.com/vikdevelop/savedesktop?tab=readme-ov-file#2-snap") if snap else None # add link to download the beta version of SaveDesktop
        dialog.set_copyright("© 2023-2024 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_artists(["Brage Fuglseth"])
        dialog.set_version(version)
        dialog.set_application_icon(icon)
        dialog.set_release_notes(rel_notes)
        dialog.present(app.get_active_window())
    
    # create Gio actions for opening the folder, logging out of the system, etc.
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
    
    # Show the main window of the application
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp()
app.run(sys.argv)
