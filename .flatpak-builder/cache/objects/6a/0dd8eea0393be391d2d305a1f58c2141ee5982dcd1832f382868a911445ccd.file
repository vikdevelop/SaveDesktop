import gi, sys, os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio
from localization import _, settings, home

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
        self.set_title(folder_name)
        self.add_suffix(self.switch)
        self.set_title_lines(4)
        self.set_activatable_widget(self.switch)
        self.set_hexpand(True)
        
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
class FlatpakAppsDialog(Adw.AlertDialog):
    def __init__(self):
        super().__init__()
        self.set_heading(_["flatpaks_data_tittle"])
        
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
