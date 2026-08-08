import gi, sys, os, configparser
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from pathlib import Path
from savedesktop.globals import *

# Row for showing available apps
class FolderSwitchRow(Adw.Bin):
    def __init__(self, folder_name):
        super().__init__()
        self.folder_name = folder_name

        # Switch row for each app
        self.switch_row = Adw.SwitchRow.new()
        self.switch_row.set_title(self.folder_name)
        self.switch_row.set_title_lines(4)
        self.switch_row.set_hexpand(True)

        # Get default state from GSettings
        if settings["disabled-flatpak-apps-data"] == []:
            self.switch_row.set_active(True)

        switch_state = self.folder_name not in settings.get_strv("disabled-flatpak-apps-data")
        self.switch_row.set_active(switch_state)

        # Connect a signal to the switch row
        self.switch_row.connect("notify::active", self.on_switch_activated)
        self.set_child(self.switch_row)

        # A mechanism that allows changing the status of a switch by clicking with the mouse on any part of the row
        gesture = Gtk.GestureClick.new()
        gesture.connect("released", self._on_row_clicked)
        self.add_controller(gesture)

        self.set_child(self.switch_row)

    def _on_row_clicked(self, gesture, n_press, x, y):
        current_state = self.switch_row.get_active()
        self.switch_row.set_active(not current_state)

    def on_switch_activated(self, switch_row, gparam):
        state = switch_row.get_active()

        appid = switch_row.get_subtitle()
        if not appid:
            appid = self.folder_name

        disabled_flatpaks = settings.get_strv("disabled-flatpak-apps-data")

        if not state:
            if appid not in disabled_flatpaks:
                disabled_flatpaks.append(appid)
        else:
            if appid in disabled_flatpaks:
                disabled_flatpaks.remove(appid)

        settings.set_strv("disabled-flatpak-apps-data", disabled_flatpaks)

# dialog for showing installed Flatpak apps
class FlatpakAppsDialog(Adw.AlertDialog):
    def __init__(self, parent, flatpaks_list=None):
        super().__init__()
        self.flatpaks_list = flatpaks_list if flatpaks_list is not None else []

        self.set_heading(_("Select Flatpak apps"))

        self.old_disabled_flatpaks = settings["disabled-flatpak-apps-data"]

        # listbox for showing items
        self.flow_box = Gtk.ListBox.new()
        self.flow_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.flow_box.set_size_request(325, -1)
        self.flow_box.add_css_class(css_class='boxed-list')

        # set self.flowbox as child for Gtk.ScrolledWindow widget
        self.set_extra_child(self.flow_box)

        # add buttons to the dialog
        self.add_response('cancel', _("Cancel"))
        self.add_response('ok', _("Apply"))
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.connect('response', self.apply_settings)

        # if there are problems loading a folder, an error message is displayed
        try:
            self.load_folders()
        except Exception as e:
            self.set_body(f"Error: {e}")

    # load items from ~/.var/app directory or archive
    def load_folders(self):
        self.var_app_dirs_num = os.listdir(f"{home}/.var/app")

        print(f"Number of apps in the .var/app dir: {len(self.var_app_dirs_num)}")
        print(f"Number of apps in the archive: {len(self.flatpaks_list)}")

        if len(self.var_app_dirs_num) > len(self.flatpaks_list):
            self._load_in_normal_mode()
        elif len(self.flatpaks_list) > len(self.var_app_dirs_num):
            self._load_in_rescue_mode()
        else:
            raise AttributeError("Found 0 apps")

    def _load_in_normal_mode(self):
        path = Path(f"{home}/.var/app")
        black_list = settings.get_strv("disabled-flatpak-apps-data")
        folders_dict = {f.name: str(f) for f in path.iterdir() if f.is_dir()}

        for name in folders_dict:
            sys_path = f"/var/lib/flatpak/app/{name}/current/active/export/share/applications/{name}.desktop"
            home_path = f"{home}/.local/share/flatpak/app/{name}/current/active/export/share/applications/{name}.desktop"
            config = configparser.ConfigParser(interpolation=None)

            if os.path.exists(sys_path):
                flatpak_path = sys_path
            elif os.path.exists(home_path):
                flatpak_path = home_path
            else:
                flatpak_path = None

            if flatpak_path:
                try:
                    with open(flatpak_path, 'r', encoding='utf-8') as f:
                        config.read_file(f)

                    app_name = config.get('Desktop Entry', f'Name[{language}]',
                                        fallback=config.get('Desktop Entry', 'Name'))

                    self.folder_row = FolderSwitchRow(app_name)
                    self.folder_row.switch_row.set_subtitle(name)
                    if name in black_list:
                        self.folder_row.switch_row.set_active(False)
                    self.flow_box.append(self.folder_row)
                except (configparser.Error, UnicodeDecodeError, IOError):
                    print(f"Error while reading: {name}")
            else:
                print(f"Desktop file doesn't exist for {name}.")

    def _load_in_rescue_mode(self):
        for app_id in self.flatpaks_list:
            self.folder_row = FolderSwitchRow(app_id)
            self.flow_box.append(self.folder_row)

    # if user clicks on the cancel button, the settings will not saved
    def apply_settings(self, w, response):
        if response == 'cancel':
            settings["disabled-flatpak-apps-data"] = self.old_disabled_flatpaks
