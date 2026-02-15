import gi, sys, os, configparser
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from pathlib import Path
from savedesktop.globals import *

# Row for showing available apps
class FolderSwitchRow(Adw.ActionRow):
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
        self.set_title(self.folder_name)
        self.add_suffix(self.switch)
        self.set_title_lines(4)
        self.set_activatable_widget(self.switch)
        self.set_hexpand(True)

        # set switch states from the Gsettings database
        switch_state = self.folder_name not in settings.get_strv("disabled-flatpak-apps-data")
        self.switch.set_active(switch_state)

    # save switch state
    def on_switch_activated(self, switch, state):
        appid = self.get_subtitle()
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
    def __init__(self, parent):
        super().__init__()
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

    # load items from ~/.var/app directory
    def load_folders(self):
        path = Path(f"{home}/.var/app")
        black_list = settings.get_strv("disabled-flatpak-apps-data")

        if path.exists():
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

                        if _("Translator credits") == "Translator credits":
                            app_name = config.get('Desktop Entry', 'Name')
                        else:
                            app_name = config.get('Desktop Entry', f'Name[{language}]')

                        self.folder_row = FolderSwitchRow(app_name)
                        self.folder_row.set_subtitle(name)
                        if name in black_list:
                            self.folder_row.switch.set_active(False)
                        self.flow_box.append(self.folder_row)
                    except (configparser.Error, UnicodeDecodeError, IOError):
                        print(f"Error while reading: {name}")
                else:
                    print(f"Desktop file doesn't exist for {name}.")
        else:
            raise FileNotFoundError(f"{home}/.var/app doesn't exist!")

    # if user clicks on the cancel button, the settings will not saved
    def apply_settings(self, w, response):
        if response == 'cancel':
            settings["disabled-flatpak-apps-data"] = self.old_disabled_flatpaks
