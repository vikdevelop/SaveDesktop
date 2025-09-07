#!/usr/bin/python3
import os, sys, re, zipfile, random, string, gi, subprocess, locale
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk
from datetime import date
from pathlib import Path
from threading import Thread
from savedesktop.globals import *
from savedesktop.gui.items_dialog import FolderSwitchRow, FlatpakAppsDialog, itemsDialog
from savedesktop.gui.more_options_dialog import MoreOptionsDialog
from savedesktop.gui.synchronization_dialogs import InitSetupDialog, SetDialog, CloudDialog
from savedesktop.core.password_store import PasswordStore

# Application window
class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Save Desktop")
        self.app_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki"

        # header bar and toolbarview
        self.headerbar = Adw.HeaderBar.new()
        self.toolbarview = Adw.ToolbarView.new()
        self.toolbarview.add_top_bar(self.headerbar)

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
        self.general_menu.append(_("Keyboard shortcuts"), 'app.shortcuts')
        self.general_menu.append(_("About app"), 'app.about')
        self.main_menu.append_section(None, self.general_menu)

        # menu button
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name(icon_name='open-menu-symbolic')
        self.menu_button.set_menu_model(menu_model=self.main_menu)
        #self.menu_button.set_tooltip_text(_("Main Menu"))
        self.menu_button.set_primary(True)
        self.headerbar.pack_end(child=self.menu_button)

        self.menu_button.set_tooltip_text(tooltip_text)

        # add Manually sync section
        if settings["manually-sync"] == True:
            self.sync_menu = Gio.Menu()
            self.sync_menu.append(_("Synchronise manually"), 'app.m-sync-with-key')
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
        self.stack.add_titled_with_icon(self.saveBox,"savepage",_("Save"),"document-save-symbolic")
        self.stack.add_titled_with_icon(self.importBox,"importpage",_("Import"),"document-open-symbolic")
        self.stack.add_titled_with_icon(self.syncingBox,"syncpage",_("Sync"),"view-refresh-symbolic") if not snap else None

        # menu switcher
        self.switcher_title = Adw.ViewSwitcherTitle.new()
        self.switcher_title.set_stack(self.stack)
        self.switcher_title.set_title("Save Desktop")
        self.headerbar.set_title_widget(self.switcher_title)

        # menu bar
        self.switcher_bar = Adw.ViewSwitcherBar.new()
        self.switcher_bar.set_stack(self.stack)
        self.toolbarview.add_bottom_bar(self.switcher_bar)

        self.setup_switcher_responsive()

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

        self._env_detection()

    # If the user has a supported environment, it shows the app window, otherwise, it shows the window with information about an unsupported environment
    def _env_detection(self):
        def setup_environment(env_name):
            self.environment = env_name
            self.save_desktop()
            self.import_desktop()
            self.sync_desktop() if not snap else print("Synchronization in the Snap environment is temporarily disabled.")
            self.connect("close-request", self.on_close)

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
            'Deepin': 'Deepin',
            'Hyprland': 'Hyprland'}

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
            self.unsupp_label = Gtk.Label.new(str=f'<big>{_("<big><b>You have an unsupported environment installed.</b></big>\nPlease use one of these environments: {}.")}</big>'.format(', '.join(set(desktop_map.values())))); self.unsupp_label.set_use_markup(True); self.unsupp_label.set_justify(Gtk.Justification.CENTER); self.unsupp_label.set_wrap(True); self.pBox.append(self.unsupp_label)

    # Switch between ViewSwitcherTitle and ViewSwitcherBar based on the title visible
    def setup_switcher_responsive(self):
        narrow_breakpoint = Adw.Breakpoint.new(
            Adw.BreakpointCondition.parse("max-width: 400sp")
        )

        # When activating a narrow breakpoint, display the switcher_bar
        narrow_breakpoint.connect("apply",
            lambda bp: self.switcher_bar.set_reveal(True))

        # Hide switcher_bar when narrow breakpoint is deactivated
        narrow_breakpoint.connect("unapply",
            lambda bp: self.switcher_bar.set_reveal(False))

        # Add a breakpoint to the window
        self.add_breakpoint(narrow_breakpoint)

        # Default state - hidden (only displayed when the breakpoint is met)
        self.switcher_bar.set_reveal(False)

    # Show main page
    def save_desktop(self):
        # Set valign for the save desktop layout
        self.saveBox.set_valign(Gtk.Align.CENTER)

        # Title image for the save page
        self.titleImage = Gtk.Image.new_from_icon_name("preferences-desktop-display-symbolic")
        self.titleImage.set_pixel_size(64)
        self.saveBox.append(self.titleImage)

        # Title "Save Current configuration" for save page and subtitle "{user_desktop}"
        self.label_title = Gtk.Label.new()
        self.label_title.set_markup('<big><b>{}</b></big>\n{}'.format(_("Save the current configuration"), self.environment))
        self.label_title.set_justify(Gtk.Justification.CENTER)
        self.saveBox.append(self.label_title)

        # Box for show these options: set the filename, set items that will be included to the config archive and periodic saving
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
        self.saveEntry.set_title(_("Set the file name"))
        self.saveEntry.set_text(settings["filename"])
        self.lbox_e.append(self.saveEntry)

        # Button for opening dialog for selecting items that will be included to the config archive
        self.itemsButton = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self.itemsButton.set_valign(Gtk.Align.CENTER)
        self.itemsButton.add_css_class("flat")
        self.itemsButton.connect("clicked", self._open_itemsDialog)

        # Action row for opening dialog for selecting items that will be included to the config archive
        self.items_row = Adw.ActionRow.new()
        self.items_row.set_title(title=_("Items to include in the configuration archive"))
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
        self.msButton.connect("clicked", self._open_more_options_dialog)

        # action row
        self.moreSettings = Adw.ActionRow.new()
        self.moreSettings.set_title(_("More options"))
        self.moreSettings.set_subtitle(f'{_("Periodic saving")}, {_("Manual saving")}')
        self.moreSettings.set_subtitle_lines(3)
        self.moreSettings.add_suffix(self.msButton)
        self.moreSettings.set_activatable_widget(self.msButton)
        self.lbox_e.append(self.moreSettings)

        # Save configuration button
        self.saveButton = Gtk.Button.new_with_label(_("Save"))
        self.saveButton.add_css_class("suggested-action")
        self.saveButton.add_css_class("pill")
        self.saveButton.connect("clicked", self.select_folder)
        self.saveButton.set_valign(Gtk.Align.CENTER)
        self.saveButton.set_halign(Gtk.Align.CENTER)
        self.saveBox.append(self.saveButton)

    def _open_more_options_dialog(self, w):
        self.more_options_dialog = MoreOptionsDialog(self)
        self.more_options_dialog.choose(self, None, None, None)
        self.more_options_dialog.present(self)

    # open a dialog for selecting the items to include in the configuration archive
    def _open_itemsDialog(self, w):
        self.itemsd = itemsDialog()
        self.itemsd.choose(self, None, None, None)
        self.itemsd.present()

    # Import configuration page
    def import_desktop(self):
        self.importBox.set_valign(Gtk.Align.CENTER)
        self.importBox.set_halign(Gtk.Align.CENTER)

        # Box for the below buttons
        self.btnBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Import configuration button
        self.fileButton = Gtk.Button.new_with_label(_("Import from file"))
        self.fileButton.add_css_class("pill")
        self.fileButton.add_css_class("suggested-action")
        self.fileButton.set_halign(Gtk.Align.CENTER)
        self.fileButton.set_valign(Gtk.Align.CENTER)
        self.fileButton.connect("clicked", self.select_file_to_import)
        self.btnBox.append(self.fileButton)

        # Import configuration from folder button
        self.folderButton = Gtk.Button.new_with_label(_("Import from folder"))
        self.folderButton.add_css_class("pill")
        self.folderButton.set_halign(Gtk.Align.CENTER)
        self.folderButton.set_valign(Gtk.Align.CENTER)
        self.folderButton.connect("clicked", self.select_folder_to_import)
        self.btnBox.append(self.folderButton)

        # Image and title for the Import page
        self.importPage = Adw.StatusPage.new()
        self.importPage.set_icon_name("document-open-symbolic")
        self.importPage.set_title(_("Import"))
        self.importPage.set_description(_("Import saved configuration"))
        self.importPage.set_size_request(360, -1)
        self.importPage.set_child(self.btnBox)
        self.importBox.append(self.importPage)

    # Syncing desktop page
    def sync_desktop(self):
        # Set showing the Initial synchronization setup dialog only if the periodic saving folder or cloud drive folder does not use GVFS or Rclone filesystem
        settings["first-synchronization-setup"] = True if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh") else False
        language = locale.getlocale()[0].split("_")[0]

        # Box, image and title for this page
        self.sync_btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.syncPage = Adw.StatusPage.new()
        self.syncPage.set_icon_name("view-refresh-symbolic")
        self.syncPage.set_title(_("Sync"))
        self.syncPage.set_description(f'{_("Sync your desktop environment configuration with other computers in the network.")} <a href="{self.app_wiki}/synchronization/{language}">{_("Learn more")}</a>')
        self.syncPage.set_child(self.sync_btn_box)
        self.syncingBox.append(self.syncPage)

        # "Set up the sync file" button
        self.setButton = Gtk.Button.new_with_label(_("Set up the sync file"))
        self.setButton.set_name("set-button")
        self.setButton.add_css_class("pill")
        self.setButton.add_css_class("suggested-action")
        self.setButton.connect("clicked", self._open_SetDialog if not settings["first-synchronization-setup"] else self._open_InitSetupDialog)
        self.setButton.set_valign(Gtk.Align.CENTER)
        self.setButton.set_halign(Gtk.Align.CENTER)
        self.sync_btn_box.append(self.setButton)

        # "Connect with other computer" button
        self.getButton = Gtk.Button.new_with_label(_("Connect to the cloud storage"))
        self.getButton.set_name("get-button")
        self.getButton.add_css_class("pill")
        self.getButton.connect("clicked", self._open_CloudDialog if not settings["first-synchronization-setup"] else self._open_InitSetupDialog)
        self.getButton.set_valign(Gtk.Align.CENTER)
        self.getButton.set_halign(Gtk.Align.CENTER)
        self.sync_btn_box.append(self.getButton)

    def _open_InitSetupDialog(self, w):
        self.get_btn_type = w.get_name()
        self.init_setup_dialog = InitSetupDialog(self)
        self.init_setup_dialog.choose(self, None, None, None)
        self.init_setup_dialog.present(self)

    def _open_SetDialog(self, w):
        self.set_dialog = SetDialog(self)
        self.set_dialog.choose(self, None, None, None)
        self.set_dialog.present(self)

    def _open_CloudDialog(self, w):
        self.set_dialog = CloudDialog(self)
        self.set_dialog.choose(self, None, None, None)
        self.set_dialog.present(self)

    # Select folder for periodic backups (Gtk.FileDialog)
    def select_pb_folder(self, w):
        def save_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except:
                return
            self.folder_pb = folder.get_path()
            settings["periodic-saving-folder"] = self.folder_pb if settings["first-synchronization-setup"] else settings["periodic-saving-folder"]
            self.dirRow.set_subtitle(f"{self.folder_pb}") if hasattr(self, 'dirRow') else None

        self.pb_chooser = Gtk.FileDialog.new()
        self.pb_chooser.set_modal(True)
        self.pb_chooser.set_title(_("Choose custom folder for periodic saving"))
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

        self.folderchooser = Gtk.FileDialog.new()
        self.folderchooser.set_modal(True)
        self.folderchooser.set_title(_("Save the current configuration"))
        self.folderchooser.select_folder(self, None, save_selected, None)

    # Select a ZIP or TAR.GZ file to import
    def select_file_to_import(self, w):
        # Show a "Please wait" pop-up window while checking the archive type
        def show_please_wait_toast():
            wait_toast = Adw.Toast.new(title=_("Please wait …"))
            wait_toast.set_timeout(10)
            self.toast_overlay.add_toast(wait_toast)

        # Check, if the archive is encrypted or not
        def get_status_of_encryption():
            self.is_folder = False
            try:
                status = any(z.flag_bits & 0x1 for z in zipfile.ZipFile(self.import_file).infolist() if not z.filename.endswith("/"))
            except:
                status = False
            if status == True:
                GLib.idle_add(self.check_password_dialog)
            else:
                self.import_config()

        # Get path from the dialog
        def open_selected(source, res, data):
            try:
                file = source.open_finish(res)
            except:
                return
            self.import_file = file.get_path()
            show_please_wait_toast()
            check_thread = Thread(target=get_status_of_encryption)
            check_thread.start()

        self.file_chooser = Gtk.FileDialog.new()
        self.file_chooser.set_modal(True)
        self.file_chooser.set_title(_("Import saved configuration"))
        self.file_filter = Gtk.FileFilter.new()
        self.file_filter.set_name(_("Save Desktop files"))
        self.file_filter.add_pattern('*.sd.tar.gz')
        self.file_filter.add_pattern('*.sd.zip')
        self.file_filter_list = Gio.ListStore.new(Gtk.FileFilter);
        self.file_filter_list.append(self.file_filter)
        self.file_chooser.set_filters(self.file_filter_list)
        self.file_chooser.open(self, None, open_selected, None)

    # Select folder to import configuration
    def select_folder_to_import(self, w):
        def import_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except:
                return
            self.import_folder = folder.get_path()
            self.is_folder = True if os.path.exists(f"{self.import_folder}/.folder.sd") else False
            self.import_config()

        self.file_chooser = Gtk.FileDialog.new()
        self.file_chooser.set_modal(True)
        self.file_chooser.set_title(_("Import saved configuration"))
        self.file_chooser.select_folder(self, None, import_selected, None)

    # Dialog for creating password for the config archive
    def create_password_dialog(self):
        # Action after closing pswdDialog
        def pswdDialog_closed(w, response):
            if response == 'ok':
                with open(f"{CACHE}/temp_file", "w") as tmp:
                    tmp.write(self.pswdEntry.get_text())
                self.save_config()

        # Check the password to see if it meets the criteria
        def check_password(pswdEntry):
            password = self.pswdEntry.get_text()
            criteria = [
                (len(password) < 12, "The password is too short. It should has at least 12 characters"),
                (not re.search(r'[A-Z]', password), "The password should has at least one capital letter"),
                (not re.search(r'[a-z]', password), "The password should has at least one lowercase letter"),
                (not re.search(r'[-_@.:,+=]', password), "The password should has at least one special character"),
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
            safe = "-_@.:,+="
            allc = safe + string.ascii_letters + string.digits
            password = [random.choice(safe), random.choice(string.ascii_letters), random.choice(string.digits)] + \
                       [random.choice(allc) for _ in range(21)]
            random.shuffle(password)
            password = ''.join(password)
            self.pswdEntry.set_text(password)

        # Dialog itself
        self.pswdDialog = Adw.AlertDialog.new()
        self.pswdDialog.set_heading(_("Create new password"))
        self.pswdDialog.set_body(_("Please create new password for your archive. Criteria include a length of at least 12 characters, one uppercase letter, one lowercase letter, and one special character."))
        self.pswdDialog.choose(self, None, None, None)
        self.pswdDialog.add_response("cancel", _("Cancel"))
        self.pswdDialog.add_response("ok", _("Apply"))
        self.pswdDialog.set_response_enabled("ok", False)
        self.pswdDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.pswdDialog.connect('response', pswdDialog_closed)
        self.pswdDialog.present()

        # Button for generating strong password
        self.pswdgenButton = Gtk.Button.new_from_icon_name("dialog-password-symbolic")
        self.pswdgenButton.set_tooltip_text(_("Generate Password"))
        self.pswdgenButton.add_css_class("flat")
        self.pswdgenButton.set_valign(Gtk.Align.CENTER)
        self.pswdgenButton.connect("clicked", pswd_generator)

        # entry for entering password
        self.pswdEntry = Adw.PasswordEntryRow.new()
        self.pswdEntry.set_title(_("Password"))
        self.pswdEntry.connect('changed', check_password)
        self.pswdEntry.add_suffix(self.pswdgenButton)
        self.pswdDialog.set_extra_child(self.pswdEntry)

    # Save configuration
    def save_config(self):
        self.archive_mode = "--create"
        self.archive_name = f"{self.folder}/{self.filename_text}"
        self.please_wait_save()
        save_thread = Thread(target=self._call_archive_command)
        save_thread.start()

    def _call_archive_command(self):
        try:
            subprocess.run([sys.executable, "-m", "savedesktop.core.archive", self.archive_mode, self.archive_name], check=True, env={**os.environ, "PYTHONPATH": "/app/share/savedesktop"})
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.show_err_msg, e)
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(self.switcher_title.get_title_visible())
        finally:
            if self.archive_mode == "--create":
                GLib.idle_add(self.exporting_done)
            elif self.archive_mode == "--unpack":
                GLib.idle_add(self.applying_done)
            else:
                pass

    # "Please wait" information page on the "Save" page
    def please_wait_save(self):
        # Stop saving configuration
        def cancel_save(w):
            os.popen('pkill -f "savedesktop.core.config"')
            os.popen(f"pkill -9 7z")
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(True if self.switcher_title.get_title_visible() else False)
            self.set_title("Save Desktop")
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
        self.set_title(_("<big><b>Saving configuration …</b></big>\nThe configuration of your desktop environment will be saved in:\n<i>{}/{}.sd.tar.gz</i>").split('</b>')[0].split('<b>')[-1])

        # Create spinner for this page
        self.savewaitSpinner = Gtk.Spinner.new()
        self.savewaitSpinner.set_size_request(100, 100)
        self.savewaitSpinner.start()
        self.savewaitBox.append(self.savewaitSpinner)

        # Prepare Gtk.Image widget for the next page
        self.sdoneImage = Gtk.Image.new()
        self.savewaitBox.append(self.sdoneImage)

        # Use "sd.zip" if Archive Encryption is enabled
        status_old = _("<big><b>Saving configuration …</b></big>\nThe configuration of your desktop environment will be saved in:\n<i>{}/{}.sd.tar.gz</i>")
        status = status_old.replace("sd.tar.gz", "sd.zip") if not settings["save-without-archive"] else status_old.replace("sd.tar.gz", "")

        # Create label about selected directory for saving the configuration
        self.savewaitLabel = Gtk.Label.new(str=status.format(self.folder, self.filename_text))
        self.savewaitLabel.set_use_markup(True)
        self.savewaitLabel.set_justify(Gtk.Justification.CENTER)
        self.savewaitLabel.set_wrap(True)
        self.savewaitBox.append(self.savewaitLabel)

        # Create button for cancel saving configuration
        self.savewaitButton = Gtk.Button.new_with_label(_("Cancel"))
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
            self.switcher_bar.set_reveal(True if self.switcher_title.get_title_visible() else False)
            self.set_title("Save Desktop")
            for widget in [self.savewaitSpinner, self.savewaitLabel, self.savewaitButton, self.sdoneImage, self.opensaveButton, self.backtomButton]:
                self.savewaitBox.remove(widget)

        # send notification about saved configuration if application window is inactive only
        self.notification_save = Gio.Notification.new("SaveDesktop")
        self.notification_save.set_body(_("Configuration has been saved!"))
        app = self.get_application()
        active_window = app.get_active_window()
        if active_window is None or not active_window.is_active():
            app.send_notification(None, self.notification_save)

        # stop spinner animation
        self.savewaitSpinner.stop()
        self.savewaitBox.remove(self.savewaitButton)
        self.savewaitBox.remove(self.savewaitSpinner)

        # set title to "Configuration has been saved!"
        self.set_title(_("Configuration has been saved!"))

        # use widget for showing done.svg icon
        self.sdoneImage.set_from_icon_name("done")
        self.sdoneImage.set_pixel_size(128)

        # edit label for the purposes of this page
        self.savewaitLabel.set_label(_("<big><b>{}</b></big>\nYou can now view the archive with the configuration of your desktop environment, or return to the previous page.").format(_("Configuration has been saved!")))
        self.opensaveButton = Gtk.Button.new_with_label(_("Open the folder"))
        self.opensaveButton.add_css_class('pill')
        self.opensaveButton.add_css_class('suggested-action')
        self.opensaveButton.set_action_name("app.open_dir")
        self.opensaveButton.set_valign(Gtk.Align.CENTER)
        self.opensaveButton.set_halign(Gtk.Align.CENTER)
        self.savewaitBox.append(self.opensaveButton)

        # create button for backing to the previous page
        self.backtomButton = Gtk.Button.new_with_label(_("Back to previous page"))
        self.backtomButton.connect("clicked", back_to_main)
        self.backtomButton.add_css_class("pill")
        self.backtomButton.set_valign(Gtk.Align.CENTER)
        self.backtomButton.set_halign(Gtk.Align.CENTER)
        self.savewaitBox.append(self.backtomButton)

    # dialog for entering password of the archive
    def check_password_dialog(self):
        # action after closing dialog for checking password
        def checkDialog_closed(w, response):
            if response == 'ok':
                self.checkDialog.set_response_enabled("ok", False)
                with open(f"{CACHE}/temp_file", "w") as tmp:
                    tmp.write(self.checkEntry.get_text())

                self.import_config()

        # Dialog itself
        self.checkDialog = Adw.AlertDialog.new()
        self.checkDialog.set_heading(_("Unlock the archive with a password"))
        self.checkDialog.set_body(_("Enter the password below to unlock the archive with your configuration. If you have forgotten it, you will not be able to unzip the archive and start importing your configuration."))
        self.checkDialog.choose(self, None, None, None)
        self.checkDialog.add_response("cancel", _("Cancel"))
        self.checkDialog.add_response("ok", _("Apply"))
        self.checkDialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.checkDialog.connect('response', checkDialog_closed)
        self.checkDialog.present()

        self.checkEntry = Adw.PasswordEntryRow.new()
        self.checkEntry.set_title(_("Password"))
        self.checkDialog.set_extra_child(self.checkEntry)

    # Import configuration
    def import_config(self):
        self.archive_mode = "--unpack"
        self._identify_file_type()
        self.please_wait_import()
        import_thread = Thread(target=self._call_archive_command)
        import_thread.start()

    def _identify_file_type(self):
        try:
            self.archive_name = self.import_folder
        except:
            self.archive_name = self.import_file

    # "Please wait" information on the "Import" page
    def please_wait_import(self):
        # Stop importing configuration
        def cancel_import(w):
            os.popen("pkill -9 7z")
            os.popen("pkill -9 tar")
            os.popen('pkill -f "savedesktop.core.config"')
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(True if self.switcher_title.get_title_visible() else False)
            self.set_title("Save Desktop")
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
        self.set_title(_("<big><b>Importing configuration …</b></big>\nImporting configuration from:\n<i>{}</i>").split('</b>')[0].split('<b>')[-1])

        # Create spinner for this page
        self.importwaitSpinner = Gtk.Spinner.new()
        self.importwaitSpinner.set_size_request(100, 100)
        self.importwaitSpinner.start()
        self.importwaitBox.append(self.importwaitSpinner)

        # Prepare Gtk.Image widget for this page
        self.idoneImage = Gtk.Image.new()
        self.importwaitBox.append(self.idoneImage)

        # Create label about configuration archive name
        try:
            self.importwaitLabel = Gtk.Label.new(str=_("<big><b>Importing configuration …</b></big>\nImporting configuration from:\n<i>{}</i>").format(self.import_file))
        except:
            self.importwaitLabel = Gtk.Label.new(str=_("<big><b>Importing configuration …</b></big>\nImporting configuration from:\n<i>{}</i>").format(self.import_folder))
        self.importwaitLabel.set_use_markup(True)
        self.importwaitLabel.set_justify(Gtk.Justification.CENTER)
        self.importwaitLabel.set_wrap(True)
        self.importwaitBox.append(self.importwaitLabel)

        # Create button for canceling importing configuration
        self.importwaitButton = Gtk.Button.new_with_label(_("Cancel"))
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
            self.switcher_bar.set_reveal(True if self.switcher_title.get_title_visible() else False)
            self.set_title("Save Desktop")
            [self.importwaitBox.remove(widget) for widget in [self.importwaitSpinner, self.importwaitLabel, self.importwaitButton, self.idoneImage, self.logoutButton, self.backtomButton]]
            if hasattr(self, 'flistBox'):
                self.pBox.remove(self.flistBox)

        # send notification about imported configuration if application window is inactive only
        self.notification_import = Gio.Notification.new("Save Desktop")
        self.notification_import.set_body(_("The configuration has been applied!"))
        app = self.get_application()
        active_window = app.get_active_window()
        if active_window is None or not active_window.is_active():
            app.send_notification(None, self.notification_import)

        # stop spinner animation
        self.importwaitSpinner.stop()
        self.importwaitBox.remove(self.importwaitButton)
        self.importwaitBox.remove(self.importwaitSpinner)

        # set title to "Configuration has been applied!"
        self.set_title(_("The configuration has been applied!"))

        # widget for showing done.svg icon
        self.idoneImage.set_from_icon_name("done")
        self.idoneImage.set_pixel_size(128)

        # edit label for the purposes of this page
        self.importwaitLabel.set_label(_("<big><b>{}</b></big>\nYou can log out of the system for the changes to take effect, or go back to the previous page and log out later.").format(_("The configuration has been applied!")))

        # create button for loging out of the system
        self.logoutButton = Gtk.Button.new_with_label(_("Log Out"))
        self.logoutButton.add_css_class('pill')
        self.logoutButton.add_css_class('suggested-action')
        self.logoutButton.set_halign(Gtk.Align.CENTER)
        self.logoutButton.set_valign(Gtk.Align.CENTER)
        self.logoutButton.set_action_name("app.logout")
        self.importwaitBox.append(self.logoutButton) if not (flatpak and self.environment == "Hyprland") else None

        # create button for backing to the previous page
        self.backtomButton = Gtk.Button.new_with_label(_("Back to previous page"))
        self.backtomButton.connect("clicked", back_to_main)
        self.backtomButton.add_css_class("pill")
        self.backtomButton.set_halign(Gtk.Align.CENTER)
        self.backtomButton.set_valign(Gtk.Align.CENTER)
        self.importwaitBox.append(self.backtomButton)

    # show message dialog in the error case
    def show_err_msg(self, error):
        error_str = str(error)
        if "died" in error_str:
            return

        self.errDialog = Adw.AlertDialog.new()
        self.errDialog.choose(self, None, None, None)
        self.errDialog.set_heading(heading=_("An error occurred"))
        self.errDialog.set_body(body=f"{error_str}")
        self.errDialog.add_response('cancel', _("Cancel"))
        self.errDialog.present()

    # a warning indicating that the user must log out
    def show_warn_toast(self):
        self.warn_toast = Adw.Toast.new(title=_("Changes will only take effect after the next login"))
        self.warn_toast.set_button_label(_("Log Out"))
        self.warn_toast.set_action_name("app.logout")
        self.toast_overlay.add_toast(self.warn_toast)

    # message that says where will be run a synchronization
    def show_special_toast(self):
        self.special_toast = Adw.Toast.new(title=_("From now on, you can sync the config from the menu in the header bar"))
        self.toast_overlay.add_toast(self.special_toast)

    # action after closing the main window
    def on_close(self, w):
        self.close()
        # Save window size, state, and filename
        settings["window-size"] = self.get_default_size()
        settings["maximized"] = self.is_maximized()
        settings["filename"] = self.saveEntry.get_text()

        # Check for ongoing operations before clearing cache
        if any(os.path.exists(f"{CACHE}/{path}") for path in ["import_config/import_status", "syncing/sync_status", "periodic_saving/saving_status"]):
            print("saving/importing/syncing configuration in progress...")
        else:
            pass
