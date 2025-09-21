import gi, os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
from savedesktop.globals import *
from savedesktop.core.password_store import PasswordStore

class MoreOptionsDialog(Adw.AlertDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.set_heading(_("More options"))

        # Box for this dialog
        self.msBox = Gtk.ListBox.new()
        self.msBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.msBox.add_css_class('boxed-list')
        self.set_extra_child(self.msBox)

        # Periodic saving section
        # Expander row for showing options of the periodic saving
        self.periodic_row = Adw.ExpanderRow.new()
        self.periodic_row.set_title(_("Periodic saving"))
        self.msBox.append(child=self.periodic_row)

        options = Gtk.StringList.new(strings=[
            _("Never"), _("Daily"), _("Weekly"), _("Monthly")
        ])

        self.pbRow = Adw.ComboRow.new()
        self.pbRow.set_title(_("Interval"))
        self.pbRow.set_use_markup(True)
        self.pbRow.set_subtitle(_("Changes will only take effect after the next login"))
        self.pbRow.set_subtitle_lines(4)
        self.pbRow.set_model(model=options)
        self.periodic_row.add_row(self.pbRow)

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
        self.filefrmtButton.set_tooltip_text(_("Reset to default"))
        self.filefrmtButton.connect("clicked", self.reset_fileformat)

        # Entry for selecting file name format
        self.filefrmtEntry = Adw.EntryRow.new()
        self.filefrmtEntry.set_title(_("File name format"))
        self.filefrmtEntry.add_suffix(self.filefrmtButton)
        self.filefrmtEntry.set_text(settings["filename-format"])
        self.periodic_row.add_row(self.filefrmtEntry)

        # Button for choosing folder for periodic saving
        self.folderButton = Gtk.Button.new_from_icon_name("document-open-symbolic")
        self.folderButton.set_valign(Gtk.Align.CENTER)
        self.folderButton.set_tooltip_text(_("Choose another folder"))
        self.folderButton.connect("clicked", self.open_file_dialog)

        # Adw.ActionRow for showing folder for periodic saving
        self.dirRow = Adw.ActionRow.new()
        self.dirRow.set_title(_("Folder for periodic saving"))
        self.dirRow.add_suffix(self.folderButton)
        self.dirRow.set_use_markup(True)
        self.dirRow.set_subtitle(settings["periodic-saving-folder"].format(download_dir))
        self.periodic_row.add_row(self.dirRow)

        # Adw.ActionRow for entering a password for the archive encryption
        self.cpwdRow = Adw.PasswordEntryRow.new()
        self.cpwdRow.set_title(_("Password for encryption"))
        self.periodic_row.add_row(self.cpwdRow)
        self._get_password_from_file()

        # Button for generating strong password
        self.pswdgenButton = Gtk.Button.new_from_icon_name("dialog-password-symbolic")
        self.pswdgenButton.set_tooltip_text(_("Generate Password"))
        self.pswdgenButton.add_css_class("flat")
        self.pswdgenButton.set_valign(Gtk.Align.CENTER)
        self.pswdgenButton.connect("clicked", self._get_generated_password)
        self.cpwdRow.add_suffix(self.pswdgenButton)

        # Manual saving section
        self.manRow = Adw.ExpanderRow.new()
        self.manRow.set_title(_("Manual saving"))
        self.manRow.set_expanded(True)
        self.msBox.append(self.manRow)

        # action row and switch for showing options of the archive encryption
        self.encryptSwitch = Gtk.Switch.new()
        self.archSwitch = Gtk.Switch.new()
        self.encryptSwitch.set_valign(Gtk.Align.CENTER)
        self.encryptSwitch.connect('notify::active', self.set_encryptswitch_sensitivity)
        if settings["enable-encryption"] == True:
            self.encryptSwitch.set_active(True)
            self.archSwitch.set_sensitive(False)

        self.encryptRow = Adw.ActionRow.new()
        self.encryptRow.set_title(_("Archive encryption"))
        self.encryptRow.set_subtitle(f'{_("When manually saving the configuration, you will be prompted to create a password. This is useful when saving the configuration to portable media for better security of your data.")}')
        self.encryptRow.set_subtitle_lines(15)
        self.encryptRow.add_suffix(self.encryptSwitch)
        self.encryptRow.set_activatable_widget(self.encryptSwitch)
        self.manRow.add_row(self.encryptRow)

        # action row and switch for showing the "Save a configuration without creating the archive" option
        self.archSwitch.set_valign(Gtk.Align.CENTER)
        self.archSwitch.connect('notify::active', self.set_archswitch_sensitivity)
        if settings["save-without-archive"] == True:
            self.archSwitch.set_active(True)
            self.encryptSwitch.set_sensitive(False)

        self.archRow = Adw.ActionRow.new()
        self.archRow.set_title(_("Save the configuration without creating an archive"))
        self.archRow.add_suffix(self.archSwitch)
        self.archRow.set_activatable_widget(self.archSwitch)
        self.manRow.add_row(self.archRow)

        self._expand_periodic_row()

        # add response of this dialog
        self.add_response('cancel', _("Cancel"))
        self.add_response('ok', _("Apply"))
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.connect('response', self.msDialog_closed)

    def _get_password_from_file(self):
        if os.path.exists(f"{DATA}/password"):
            p = PasswordStore()
            self.cpwdRow.set_text(p.password)
        else:
            self.cpwdRow.set_text("")

    def _get_generated_password(self, w):
        self.password = self.parent._password_generator()
        self.cpwdRow.set_text(self.password)

    def open_file_dialog(self, w):
        self.parent.select_pb_folder(w="")

    # reset the file name format entry to the default value
    def reset_fileformat(self, w):
        self.filefrmtEntry.set_text("Latest_configuration")

    # set sensitivity of the encryptSwitch
    def set_encryptswitch_sensitivity(self, GParamBoolean, encryptSwitch):
        if self.encryptSwitch.get_active():
            self.archSwitch.set_sensitive(False)
        else:
            self.archSwitch.set_sensitive(True)

    # set sensitivity of the archSwitch
    def set_archswitch_sensitivity(self, GParamBoolean, archSwitch):
        if self.archSwitch.get_active():
            self.encryptSwitch.set_sensitive(False)
        else:
            self.encryptSwitch.set_sensitive(True)

    def _expand_periodic_row(self):
        if os.path.exists(f"{CACHE}/expand_pb_row"):
            self.periodic_row.set_expanded(True)
            self.manRow.set_expanded(False)

    # Action after closing dialog for showing more options
    def msDialog_closed(self, w, response):
        if response == 'ok':
            settings["filename-format"] = self.filefrmtEntry.get_text() # save the file name format entry
            settings["periodic-saving-folder"] = self.dirRow.get_subtitle() # save the selected periodic saving folder
            settings["enable-encryption"] = self.encryptSwitch.get_active() # save the archive encryption's switch state
            settings["save-without-archive"] = self.archSwitch.get_active() # save the switch state of the "Save a configuration without creating the configuration archive" option
            self._save_periodic_saving_values()
            self._save_password()
            self._call_set_dialog()

    def _save_periodic_saving_values(self):
        # save the periodic saving interval
        self.selected_item = self.pbRow.get_selected_item()
        self.backup_mapping = {_("Never"): "Never", _("Daily"): "Daily", _("Weekly"): "Weekly", _("Monthly"): "Monthly"}
        self.backup_item = self.backup_mapping.get(self.selected_item.get_string(), "Never")
        settings["periodic-saving"] = self.backup_item
        if not self.backup_item == "Never":
            self.__create_pb_desktop()

    # create desktop file for enabling periodic saving at startup
    def __create_pb_desktop(self):
        os.makedirs(f'{home}/.config/autostart', exist_ok=True)
        if not os.path.exists(f"{DATA}/savedesktop-synchronization.sh"):
            with open(f'{home}/.config/autostart/io.github.vikdevelop.SaveDesktop.Backup.desktop', 'w') as cb:
                cb.write(f'[Desktop Entry]\nName=SaveDesktop (Periodic backups)\nType=Application\nExec={periodic_saving_cmd}')

    # save the entered password to the file
    def _save_password(self):
        if self.cpwdRow.get_text():
            password = self.cpwdRow.get_text()
            PasswordStore(password)
        else:
            try:
                os.remove(f"{DATA}/password")
            except:
                pass

    def _call_set_dialog(self):
        if os.path.exists(f"{CACHE}/expand_pb_row"):
            self.parent._open_SetDialog()
