import gi, sys, subprocess, os, locale
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from threading import Thread
from gi.repository import Gtk, Gdk, Adw, GLib, Gio
from savedesktop.globals import *

class InitSetupDialog(Adw.AlertDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.cloud_dialog = CloudDialog(parent)

        # set the self.get_button_type variable before starting the dialog
        self.get_button_type = self.parent.get_btn_type

        # Dialog itself
        self.set_heading(_("Initial synchronization setup"))
        self.set_body_use_markup(True)
        self.set_can_close(False)
        self.add_response('cancel', _("Cancel"))
        #self.add_response('ok-syncthing', _("Use Syncthing folder instead"))
        self.set_response_appearance('cancel', Adw.ResponseAppearance.DESTRUCTIVE)
        self.connect('response', self.initsetupDialog_closed)

        # create a ListBox for the rows below
        self.initBox = Gtk.ListBox.new()
        self.initBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.initBox.add_css_class("boxed-list")
        self.initBox.set_vexpand(True)
        self.set_extra_child(self.initBox)

        # if the user has GNOME, Cinnamon, COSMIC (Old) or Budgie environment, it shows text about setting up GNOME Online Accounts.
        # otherwise, it shows the text about setting up Rclone
        if self.parent.environment in ["GNOME", "Cinnamon", "COSMIC (Old)", "Budgie"]:
            self.firstRow = Adw.ActionRow.new()
            self.firstRow.set_title(_("1. Open the system settings"))
            self.initBox.append(self.firstRow)

            self.secondRow = Adw.ActionRow.new()
            self.secondRow.set_title(_("2. Go to the Online Accounts section"))
            self.secondRow.set_subtitle(_("In this section select the cloud service you want, such as Google, Microsoft 365 or Nextcloud."))
            self.initBox.append(self.secondRow)

            self.thirdRow = Adw.ActionRow.new()
            self.thirdRow.set_title(_("3. Click on the Next button and select the created cloud drive folder"))
            self.thirdRow.set_subtitle(_("The created cloud drive folder can be found in the side panel of the file chooser dialog, in this form: username@service.com."))
            self.initBox.append(self.thirdRow)

            self.add_response('next', _("Next"))
            self.set_response_appearance('next', Adw.ResponseAppearance.SUGGESTED)
        else:
            self.set_body(_("For synchronization to works properly, you need to have the folder, that is synced with your cloud service using Rclone.\n<b>Start by selecting the cloud drive service you use.</b>"))

            # create a list with available services, which can be connected via Rclone
            services = Gtk.StringList.new(strings=[_("Select"), 'Google Drive', 'Microsoft OneDrive', 'DropBox', 'pCloud'])

            # row for selecting the cloud service
            self.servRow = Adw.ComboRow.new()
            self.servRow.set_model(services)
            self.servRow.connect("notify::selected-item", self._get_service)
            self.initBox.append(self.servRow)

            # button for copying the Rclone command to clipboard
            self.copyButton = Gtk.Button.new()
            self.copyButton.add_css_class('flat')
            self.copyButton.set_valign(Gtk.Align.CENTER)
            self.copyButton.set_sensitive(False)

            # row for showing the command for setting up the Rclone
            self.cmdRow = Adw.ActionRow.new()
            self.cmdRow.set_subtitle_selectable(True)
            self.cmdRow.set_use_markup(True)
            self.cmdRow.add_suffix(self.copyButton)
            self.initBox.append(self.cmdRow)

            # add the Apply and Syncthing buttons to the dialog
            self.add_response('ok-syncthing', _("Use Syncthing folder instead"))
            self.add_response('ok-rclone', _("Apply"))
            self.set_response_appearance('ok-rclone', Adw.ResponseAppearance.SUGGESTED)
            self.set_response_enabled('ok-rclone', False)

    # Responses of this dialog
    def initsetupDialog_closed(self, w, response):
        if response == 'next' or response == 'ok-syncthing': # open the Gtk.FileDialog in the GNOME Online accounts case
            self.parent.select_pb_folder(w) if self.get_button_type == 'set-button' else self.cloud_dialog.select_folder_to_sync(w)
            self.almost_done()
        elif response == 'ok-rclone': # set the periodic saving folder in the Rclone case
            if self.get_button_type == 'set-button':
                settings["periodic-saving-folder"] = f"{download_dir}/SaveDesktop/rclone_drive"
            else:
                settings["file-for-syncing"] = f"{download_dir}/SaveDesktop/rclone_drive"
            self.almost_done()
        elif response == 'cancel': # if the user clicks on the Cancel button
            self.set_can_close(True)
        elif response == 'open-setdialog': # open the "Set up the sync file" dialog after clicking on the Next button in "Almost done!" page
            self.auto_save_start = True
            settings["periodic-saving"] = "Daily"
            self.restart_app_win = True
            self.parent._open_SetDialog(w)
        elif response == 'open-clouddialog': # open the "Connect to the cloud folder" dialog after clicking on the Next button in "Almost done!" page
            settings["first-synchronization-setup"] = False
            self.restart_app_win = True
            self.parent._open_CloudDialog(w)

    # Set the Rclone setup command
    def _get_service(self, comborow, GParamObject):
        self.set_body("")
        get_servrow = self.servRow.get_selected_item().get_string()
        self.cloud_service = "drive" if get_servrow == "Google Drive" else "onedrive" if get_servrow == "Microsoft OneDrive" else "dropbox" if get_servrow == "DropBox" else "pcloud"
        self.rclone_command = f"command -v rclone &amp;> /dev/null &amp;&amp; (rclone config create savedesktop {self.cloud_service} &amp;&amp; rclone mount savedesktop: {download_dir}/SaveDesktop/rclone_drive) || echo 'Rclone is not installed. Please install it from this website first: https://rclone.org/install/.'"

        self.cmdRow.set_title(_("Now, copy the command to set up Rclone using the side button and open the terminal app using the Ctrl+Alt+T keyboard shortcut or finding it in the apps' menu."))
        self.cmdRow.set_subtitle(self.rclone_command)

        # set the copyButton properties
        self.copyButton.set_sensitive(True)
        self.copyButton.set_icon_name("edit-copy-symbolic")
        self.copyButton.set_tooltip_text(_("Copy"))
        self.copyButton.connect("clicked", self.__copy_rclone_command)

    # copy the command for setting up the Rclone using Gdk.Clipboard()
    def __copy_rclone_command(self, w):
        os.makedirs(f"{download_dir}/SaveDesktop/rclone_drive", exist_ok=True) # create the requested folder before copying the command for setting up Rclone to the clipboard

        clipboard = Gdk.Display.get_default().get_clipboard()
        Gdk.Clipboard.set(clipboard, self.rclone_command) # copy the command for setting up Rclone to the clipboard

        self.set_extra_child(None)
        self.set_body(_("Once you have finished setting up Rclone using the command provided, click the \"Apply\" button"))

        self.set_response_enabled('ok-rclone', True)
        self.remove_response('ok-syncthing')

    # show the message about finished setup the synchronization
    def almost_done(self):
        self.remove_response('ok-rclone')
        self.remove_response('next')
        self.remove_response('ok-syncthing')

        self.set_extra_child(None)
        self.set_heading(_("Almost done!"))
        self.set_body(_("You've now created the cloud drive folder! Click on the Next button to complete the setup."))
        self.set_can_close(True)

        self.add_response('open-setdialog', _("Next")) if self.get_button_type == 'set-button' else self.add_response('open-clouddialog', _("Next"))
        self.set_response_appearance('open-setdialog', Adw.ResponseAppearance.SUGGESTED) if self.get_button_type == 'set-button' else self.set_response_appearance('open-clouddialog', Adw.ResponseAppearance.SUGGESTED)

class SetDialog(Adw.AlertDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.app_wiki = "https://vikdevelop.github.io/SaveDesktop/wiki"
        self._create_file_to_expand_row()

        # Dialog itself
        self.set_heading(_("Set up the sync file"))
        self.set_body(_("Please wait …"))
        self.set_body_use_markup(True)
        self.add_response('cancel', _("Cancel"))
        self.add_response('ok', _("Apply"))
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.connect('response', self.setDialog_closed)

        # List Box for appending widgets
        self.l_setdBox = Gtk.ListBox.new()
        self.l_setdBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.l_setdBox.get_style_context().add_class('boxed-list')
        self.l_setdBox.set_size_request(-1, 160)
        self.set_extra_child(self.l_setdBox)

        # Check the synchronization matters
        check_thread = Thread(target=self.check_filesystem_fnc)
        check_thread.start()

        # Button for opening More options dialog
        self.ps_button = Gtk.Button.new_with_label(_("Change"))
        self.ps_button.connect('clicked', self.parent._open_more_options_dialog)
        self.ps_button.set_valign(Gtk.Align.CENTER)

        # Row for showing the selected periodic saving interval
        ## translate the periodic-saving key to the user language
        pb = next((key for key, value in {_("Never"): "Never", _("Daily"): "Daily", _("Weekly"): "Weekly", _("Monthly"): "Monthly"}.items() if settings["periodic-saving"] == value), None)
        self.ps_row = Adw.ActionRow.new()
        self.ps_row.set_title(f'{_("Periodic saving")} ({_("Interval")})')
        self.ps_row.set_use_markup(True)
        self.ps_row.add_suffix(self.ps_button)
        self.ps_row.set_subtitle(f'<span color="red">{_("Never")}</span>' if settings["periodic-saving"] == "Never"
                                 else f'<span color="green">{pb}</span>')
        self.ps_button.add_css_class('suggested-action') if settings["periodic-saving"] == "Never" else None

    # Create this file to set expanding the "Periodic saving" row in the More options dialog
    def _create_file_to_expand_row(self):
        open(f"{CACHE}/expand_pb_row", "w").close()

    # Refer to the article about synchronization
    def _open_sync_link(self, w):
        language = locale.getlocale()[0].split("_")[0]
        os.system(f"xdg-open {self.app_wiki}/synchronization/{language}")

    # Check the file system of the periodic saving folder and their existation
    def check_filesystem_fnc(self):
        global folder, path, check_filesystem
        check_filesystem = subprocess.getoutput('df -T "%s" | awk \'NR==2 {print $2}\'' % settings["periodic-saving-folder"])

        path = f'{settings["periodic-saving-folder"]}/{settings["filename-format"].replace(" ", "_")}.sd.zip'

        # Check if periodic saving is set to "Never"
        if settings["periodic-saving"] == "Never":
            folder = f'<span color="red">{_("Interval")}: {_("Never")}</span>'
        # Check if the filesystem is not FUSE
        elif ("gvfsd" not in check_filesystem and "rclone" not in check_filesystem) and not os.path.exists(f"{settings['periodic-saving-folder']}/.stfolder"):
            err = _("You didn't select the cloud drive folder!")
            folder = f'<span color="red">{err}</span>'
        # Check if the periodic saving file exists
        elif not os.path.exists(path):
            folder = f'<span color="red">{_("Periodic saving file does not exist.")}</span>'
        else:
            folder = path

        self.update_gui()

    def update_gui(self):
        global folder, path, check_filesystem
        self.file_row = Adw.ActionRow()
        self.file_row.set_title(_("Periodic saving file"))
        self.file_row.set_subtitle(folder)
        self.file_row.add_suffix(Gtk.Image.new_from_icon_name("network-wired-symbolic")) if "red" not in folder else None
        self.file_row.set_subtitle_lines(8)
        self.file_row.set_use_markup(True)
        self.file_row.set_subtitle_selectable(True)
        self.l_setdBox.append(self.file_row)
        self.l_setdBox.append(self.ps_row)

        set_button_sensitive = settings["periodic-saving"] != "Never" and not os.path.exists(path)
        if "red" in folder:
            self.set_response_enabled('ok', False)
            [os.remove(path) for path in [f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.sync.desktop", f"{DATA}/savedesktop-synchronization.sh"] if os.path.exists(path)] # remove these files if the periodic saving folder is not a cloud drive folder
        if _("Periodic saving file does not exist.") in folder:
            self.setupButton = Gtk.Button.new_with_label(_("Create"))
            self.setupButton.set_valign(Gtk.Align.CENTER)
            self.setupButton.add_css_class("suggested-action")
            self.setupButton.connect("clicked", self._make_pb_file)
            self.file_row.add_suffix(self.setupButton)

        if _("You didn't select the cloud drive folder!") in folder:
            self.lmButton = Gtk.Button.new_with_label(_("Learn more"))
            self.lmButton.set_valign(Gtk.Align.CENTER)
            self.lmButton.add_css_class("suggested-action")
            self.lmButton.connect("clicked", self._open_sync_link)
            self.file_row.add_suffix(self.lmButton)
        self.set_body("") # set the body as empty after loading the periodic saving information

    # make the periodic saving file if it does not exist
    def _make_pb_file(self, w):
        self.setupButton.set_sensitive(False)
        pb_thread = Thread(target=self.__save_now)
        pb_thread.start()

    def __save_now(self):
        try:
            e_o = False
            self.file_row.set_subtitle(_("Please wait …"))
            self.file_row.set_use_markup(False)
            subprocess.run(['notify-send', 'Save Desktop', _("Please wait …")])
            subprocess.run([sys.executable, "-m", "savedesktop.core.periodic_saving", "--now"], check=True, capture_output=True, text=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})
        except Exception as e:
            e_o = True
            subprocess.run(['notify-send', _("An error occurred"), f'{e.stderr}'])
            self.file_row.set_subtitle(f'{e.stderr}')
        finally:
            if not e_o:
                self.file_row.remove(self.setupButton)
                self.file_row.set_subtitle(f'{settings["periodic-saving-folder"]}/{settings["filename-format"]}.sd.zip')
                os.system(f"notify-send 'SaveDesktop' '{_('Configuration has been saved!')}'")
                self.set_response_enabled('ok', True)

    # Action after closing dialog for setting synchronization file
    def setDialog_closed(self, w, response):
        if response == 'ok':
            thread = Thread(target=self._save_file)
            thread.start()
        else:
            if os.path.exists(f"{CACHE}/expand_pb_row"):
                os.remove(f"{CACHE}/expand_pb_row")

    # save the SaveDesktop.json file to the periodic saving folder and set up the auto-mounting the cloud drive
    def _save_file(self):
        try:
            self.mount_type = "periodic-saving"
            open(f"{settings['periodic-saving-folder']}/SaveDesktop.json", "w").write('{\n "periodic-saving-interval": "%s",\n "filename": "%s"\n}' % (settings["periodic-saving"], settings["filename-format"]))
            subprocess.run([sys.executable, "-m", "savedesktop.core.synchronization_setup", "--automount-setup", self.mount_type], check=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})
        except Exception as e:
            os.system(f"notify-send \'{_('An error occurred')}\' '{e}'")
        finally:
            pass

class CloudDialog(Adw.AlertDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.set_heading(_("Connect to the cloud storage"))
        self.set_body(_("On another computer, open the Save Desktop app, and on this page, click on the \"Set up the sync file\" button and make the necessary settings. On this computer, select the folder that you have synced with your cloud storage and also have saved the same periodic saving file."))
        self.add_response('cancel', _("Cancel"))
        self.add_response('ok', _("Apply"))
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.connect('response', self.cloudDialog_closed)

        # Box for adding widgets in this dialog
        self.cloudBox = Gtk.ListBox.new()
        self.cloudBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.cloudBox.get_style_context().add_class(class_name='boxed-list')
        self.cloudBox.set_size_request(-1, 300)
        self.set_extra_child(self.cloudBox)

        # Row and buttons for selecting the cloud drive folder
        ## button for selecting the cloud drive folder
        self.cloudButton = Gtk.Button.new_from_icon_name("document-open-symbolic")
        self.cloudButton.add_css_class('flat')
        self.cloudButton.set_valign(Gtk.Align.CENTER)
        self.cloudButton.set_tooltip_text(_("Choose another folder"))
        self.cloudButton.connect("clicked", self.select_folder_to_sync)

        ## button for reseting the selected cloud drive folder
        self.resetButton = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        self.resetButton.add_css_class('destructive-action')
        self.resetButton.connect("clicked", self.reset_cloud_folder)
        self.resetButton.set_tooltip_text(_("Reset to default"))
        self.resetButton.set_valign(Gtk.Align.CENTER)

        ## the row itself
        self.cfileRow = Adw.ActionRow.new()
        self.cfileRow.add_suffix(self.resetButton) if not settings["file-for-syncing"] == "" else None
        self.cfileRow.set_title(_("Select the cloud drive folder"))
        self.cfileRow.set_subtitle(settings["file-for-syncing"])
        self.cfileRow.set_subtitle_selectable(True)
        self.cfileRow.add_suffix(self.cloudButton)
        self.cfileRow.set_activatable_widget(self.cloudButton)
        self.cloudBox.append(self.cfileRow)

        if not self.cfileRow.get_subtitle():
            self.set_response_enabled('ok', False)
        else:
            self.set_response_enabled('ok', True)

        # Periodic sync section
        options = Gtk.StringList.new(strings=[
           _("Never"), _("Manually"), _("Daily"), _("Weekly"), _("Monthly")
        ])

        self.psyncRow = Adw.ComboRow.new()
        self.psyncRow.set_use_markup(True)
        self.psyncRow.set_use_underline(True)
        self.psyncRow.set_title(_("Periodic synchronization"))
        self.psyncRow.set_title_lines(2)
        self.psyncRow.set_model(model=options)
        self.psyncRow.connect('notify::selected-item', self.on_psync_changed)
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
        self.bsyncRow.set_title(_("Bidirectional synchronization"))
        self.bsyncRow.set_subtitle(_("If enabled, and the sync interval and cloud drive folder are selected, the periodic saving information (interval, folder, and file name) from the other computer with synchronization set to synchronize is copied to this computer."))
        self.bsyncRow.set_title_lines(2)
        self.bsyncRow.add_suffix(self.bsSwitch)
        self.bsyncRow.set_activatable_widget(self.bsSwitch)
        self.cloudBox.append(self.bsyncRow)

    # Select folder for syncing the configuration with other computers in the network
    def select_folder_to_sync(self, w):
        def set_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except:
                return
            self.sync_folder = folder.get_path()
            settings["file-for-syncing"] = self.sync_folder if settings["first-synchronization-setup"] else settings["file-for-syncing"]
            self.cfileRow.set_subtitle(self.sync_folder) if hasattr(self, 'cfileRow') else None
            if hasattr(self, 'cloudDialog'):
                self.cloudDialog.set_response_enabled('ok', True) if not self.psyncRow.get_selected_item().get_string() == _("Never") else None

        self.sync_folder_chooser = Gtk.FileDialog.new()
        self.sync_folder_chooser.set_modal(True)
        self.sync_folder_chooser.set_title(_("Select the cloud drive folder"))
        self.sync_folder_chooser.select_folder(self.parent, None, set_selected, None)

    def reset_cloud_folder(self, w):
        self.cfileRow.set_subtitle("")
        self.cfileRow.remove(self.resetButton)
        self.set_response_enabled('ok', True)
        settings["file-for-syncing"] = self.cfileRow.get_subtitle()
        [os.remove(path) for path in [f"{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.sync.desktop", f"{DATA}/savedesktop-synchronization.sh"] if os.path.exists(path)]

    # enable or disable the response of this dialog in depending on the selected periodic synchronization interval
    def on_psync_changed(self, psyncRow, GParamObject):
        if not self.psyncRow.get_selected_item().get_string() == _("Never") and not self.cfileRow.get_subtitle():
            self.set_response_enabled('ok', True)

    # Action after closing URL dialog
    def cloudDialog_closed(self, w, response):
        if response == 'ok':
            self.check_psync = settings["periodic-import"]
            # translate the periodic sync options to English
            selected_item = self.psyncRow.get_selected_item()
            sync = {_("Never"): "Never2", _("Manually"): "Manually2", _("Daily"): "Daily2", _("Weekly"): "Weekly2", _("Monthly"): "Monthly2"}

            sync_item = sync.get(selected_item.get_string(), "Never2")

            settings["periodic-import"] = sync_item

            # if the selected periodic saving interval is "Manually2", it enables the manually-sync value
            settings["manually-sync"] = True and settings["periodic-import"] == "Manually2"

            # save the status of the Bidirectional Synchronization switch
            settings["bidirectional-sync"] = self.bsSwitch.get_active()

            check_thread = Thread(target=self._call_automount)
            check_thread.start()

    def _call_automount(self):
        try:
            if self.cfileRow.get_subtitle():
                self.mount_type = "cloud-receiver"
                settings["file-for-syncing"] = self.cfileRow.get_subtitle()
                result = subprocess.run([sys.executable, "-m", "savedesktop.core.synchronization_setup", "--checkfs"],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONPATH": f"{app_prefix}"})

                if result.returncode == 0:
                    output = result.stdout.strip()
                    if "You didn't selected the cloud drive folder!" in output:
                        settings["file-for-syncing"] = ""
                        if os.path.exists(f"{DATA}/savedesktop-synchronization.sh"):
                            os.remove(f"{DATA}/savedesktop-synchronization.sh")
                        raise AttributeError(_("You didn't select the cloud drive folder!"))
                    else:
                        subprocess.run([sys.executable, "-m", "savedesktop.core.synchronization_setup",
                                       "--automount-setup", self.mount_type],
                                       env={**os.environ, "PYTHONPATH": f"{app_prefix}"})
            else:
                raise AttributeError(_("You didn't select the cloud drive folder!"))
        except Exception as e:
            os.system(f'notify-send \'{_("An error occurred")}\' \'{e}\'')
            return
        else:
            GLib.idle_add(self.__post_setup)

    # check if the selected periodic sync interval was Never: if yes, shows the message about the necessity to log out of the system
    def __post_setup(self):
        if self.check_psync == "Never2":
            if not settings["periodic-import"] == "Never2":
                self.parent.show_warn_toast()

        # if it is selected to manually sync, it creates an option in the app menu in the header bar
        if settings["manually-sync"]:
            self.sync_menu = Gio.Menu()
            self.sync_menu.append(_("Synchronise manually"), 'app.m-sync-with-key')
            self.parent.main_menu.prepend_section(None, self.sync_menu)
            self.parent.show_special_toast()
        else:
            try:
                self.sync_menu.remove_all()
            except:
                pass

