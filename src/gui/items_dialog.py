import gi, sys, os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
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
    def __init__(self, parent):
        super().__init__()
        self.set_heading(_("Flatpak apps data selection"))
        
        self.old_disabled_flatpaks = settings["disabled-flatpak-apps-data"]
        
        # widget for scrolling items list
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_width(300)
        self.scrolled_window.set_min_content_height(380)
        self.set_extra_child(self.scrolled_window)
        
        # listbox for showing items
        self.flow_box = Gtk.ListBox.new()
        self.flow_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.flow_box.add_css_class(css_class='boxed-list')
        self.set_extra_child(self.flow_box)
        
        # set self.flowbox as child for Gtk.ScrolledWindow widget
        self.scrolled_window.set_child(self.flow_box)
        
        # add buttons to the dialog
        self.add_response('cancel', _("Cancel"))
        self.add_response('ok', _("Apply"))
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
                self.flow_box.append(folder_row)
        except Exception as e:
            print(f"Error loading folders: {e}")
       
    # set default switch state
    def set_initial_switch_state(self):
        disabled_flatpaks = settings.get_strv("disabled-flatpak-apps-data")
        for child in self.flow_box.get_row_at_index(0):
            if isinstance(child, FolderSwitchRow):
                child.switch.set_active(child.folder_name not in disabled_flatpaks)
    
    # if user clicks on the cancel button, the settings will not saved
    def apply_settings(self, w, response):
        if response == 'cancel':
            settings["disabled-flatpak-apps-data"] = self.old_disabled_flatpaks
            
class itemsDialog(Adw.AlertDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.set_heading(_("Select configuration items"))
        self.set_body(_("These settings are used for manual and periodic saves, imports, and synchronization."))
        
        # Box for loading widgets in this dialog
        self.itemsBox = Gtk.ListBox.new()
        self.itemsBox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.itemsBox.get_style_context().add_class(class_name='boxed-list')
        self.set_extra_child(self.itemsBox)
        
        # Switch and row of option 'Save icons'
        self.switch_01 = Gtk.Switch.new()
        if settings["save-icons"]:
            self.switch_01.set_active(True)
        self.switch_01.set_valign(align=Gtk.Align.CENTER)
        
        self.icons_row = Adw.ActionRow.new()
        self.icons_row.set_title(title=_("Icons"))
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
        self.themes_row.set_title(title=_("Themes"))
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
        self.fonts_row.set_title(title=_("Fonts"))
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
        self.backgrounds_row.set_title(title=_("Backgrounds"))
        self.backgrounds_row.set_use_markup(True)
        self.backgrounds_row.set_title_lines(2)
        self.backgrounds_row.set_subtitle_lines(3)
        self.backgrounds_row.add_suffix(self.switch_04)
        self.backgrounds_row.set_activatable_widget(self.switch_04)
        self.itemsBox.append(child=self.backgrounds_row)
        
        # show extension switch and row if user has installed these environments
        if environment["de_name"] in ["GNOME", "Cinnamon", "COSMIC (Old)", "KDE Plasma"]:
            self.save_ext_switch_state = True
            self.show_extensions_row()
        
        # Switch and row of option 'Save Desktop' (~/Desktop)
        self.switch_de = Gtk.Switch.new()
        if settings["save-desktop-folder"]:
            self.switch_de.set_active(True)
        self.switch_de.set_valign(align=Gtk.Align.CENTER)
        
        self.desktop_row = Adw.ActionRow.new()
        self.desktop_row.set_title(title=_("Desktop"))
        self.desktop_row.set_tooltip_text(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP))
        self.desktop_row.set_subtitle_selectable(True)
        self.desktop_row.set_use_markup(True)
        self.desktop_row.set_title_lines(2)
        self.desktop_row.add_suffix(self.switch_de)
        self.desktop_row.set_activatable_widget(self.switch_de)
        self.itemsBox.append(child=self.desktop_row)
        
        # Switch and row of the option: GTK Settings
        if environment["de_name"] in ["GNOME", "Cinnamon", "Xfce", "Budgie", "Pantheon", "MATE", "COSMIC (Old)"]:
            self.switch_gtk = Gtk.Switch.new()
            if settings["save-bookmarks"]:
                self.switch_gtk.set_active(True)
            self.switch_gtk.set_valign(align=Gtk.Align.CENTER)

            self.gtk_row = Adw.ActionRow.new()
            self.gtk_row.set_title(title=_("File manager bookmarks"))
            self.gtk_row.set_subtitle_selectable(True)
            self.gtk_row.set_use_markup(True)
            self.gtk_row.set_title_lines(2)
            self.gtk_row.set_subtitle_lines(3)
            self.gtk_row.add_suffix(self.switch_gtk)
            self.gtk_row.set_activatable_widget(self.switch_gtk)
            self.itemsBox.append(child=self.gtk_row)

        if flatpak:
            self.flatpak_row = Adw.ExpanderRow.new()
            self.flatpak_row.set_title(title=_("Flatpak apps"))
            self.flatpak_row.set_subtitle(f"<a href='https://vikdevelop.github.io/SaveDesktop/wiki/flatpak_apps/{language}'>{_('Learn more')}</a>")
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
            self.list_row.set_title(title=_("List of installed Flatpak apps"))
            self.list_row.set_use_markup(True)
            self.list_row.set_title_lines(4)
            self.list_row.add_suffix(self.switch_05)
            self.list_row.set_activatable_widget(self.switch_05)
            self.flatpak_row.add_row(child=self.list_row)
            
            # Switch, button and row of option 'Save SaveDesktop app settings'
            self.switch_06 = Gtk.Switch.new()
            self.appsButton = Gtk.Button.new_from_icon_name("go-next-symbolic")
            
            self.data_row = Adw.ActionRow.new()
            self.data_row.set_title(title=_("User data of installed Flatpak apps"))
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
            self.switch_06.connect('notify::active', self.show_appsbtn)
            
            self.appsButton.add_css_class("flat")
            self.appsButton.set_valign(Gtk.Align.CENTER)
            self.appsButton.set_tooltip_text(_("Flatpak apps data selection"))
            self.appsButton.connect("clicked", self.manage_data_list)

            self.switch_07 = Gtk.Switch.new()
            self.switch_07.set_valign(Gtk.Align.CENTER)
            if settings["keep-flatpaks"]:
                self.switch_07.set_active(True)

            self.remove_row = Adw.ActionRow.new()
            self.remove_row.set_title(_("Keep existing Flatpak apps and data"))
            self.remove_row.set_title_lines(3)
            self.remove_row.add_suffix(self.switch_07)
            self.remove_row.set_activatable_widget(self.switch_07)
            self.flatpak_row.add_row(child=self.remove_row)

            if not self.switch_05.get_active():
                self.switch_06.set_sensitive(False)
                self.switch_06.set_active(False)
                self.switch_07.set_sensitive(False)
                self.switch_07.set_active(True)
                settings["save-flatpak-data"] = False
                settings["keep-flatpaks"] = True

            self.switch_05.connect('notify::active', self._set_sw05_sensitivity)
        
        self.add_response('cancel', _("Cancel"))
        self.add_response('ok', _("Apply"))
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)
        self.connect('response', self.itemsdialog_closed)
        
    def _set_sw05_sensitivity(self, GParamBoolean, switch_05):
        if not self.switch_05.get_active():
            self.switch_06.set_sensitive(False)
            self.switch_06.set_active(False)
            self.switch_07.set_sensitive(False)
            self.switch_07.set_active(True)
        else:
            self.switch_06.set_sensitive(True)
            self.switch_07.set_sensitive(True)

    # Action after closing itemsDialog
    def itemsdialog_closed(self, w, response):
        if response == 'ok':
            # Saving the selected options to GSettings database
            settings["save-icons"] = self.switch_01.get_active()
            settings["save-themes"] = self.switch_02.get_active()
            settings["save-fonts"] = self.switch_03.get_active()
            settings["save-backgrounds"] = self.switch_04.get_active()
            settings["save-desktop-folder"] = self.switch_de.get_active()
            settings["save-bookmarks"] = self.switch_gtk.get_active()
            settings["keep-flatpaks"] = self.switch_07.get_active()
            if flatpak:
                settings["save-installed-flatpaks"] = self.switch_05.get_active()
                settings["save-flatpak-data"] = self.switch_06.get_active()
            if self.save_ext_switch_state == True:
                settings["save-extensions"] = self.switch_ext.get_active()
                self.save_ext_switch_state = False
        elif response == 'cancel':
            if flatpak:
                switch_status = self.flatpak_data_sw_state
                settings["save-flatpak-data"] = switch_status

    # show dialog for managing Flatpak applications data
    def manage_data_list(self, w):
        self.close()
        self.appd = FlatpakAppsDialog(self.parent)
        self.appd.choose(self.parent, None, None, None)
        self.appd.present(self.parent)

    # show button after clicking on the switch "User data of Flatpak apps"
    def show_appsbtn(self, w, GParamBoolean):
        self.flatpak_data_sw_state = settings["save-flatpak-data"]
        if self.switch_06.get_active() == True:
            self.data_row.add_suffix(self.appsButton)
        else:
            self.data_row.remove(self.appsButton)
        settings["save-flatpak-data"] = self.switch_06.get_active()

    # show extensions row, if user has installed GNOME, Cinnamon or KDE Plasma DE
    def show_extensions_row(self):
        # Switch and row of option 'Save extensions'
        self.switch_ext = Gtk.Switch.new()
        if settings["save-extensions"]:
            self.switch_ext.set_active(True)
        self.switch_ext.set_valign(align=Gtk.Align.CENTER)

        self.ext_row = Adw.ActionRow.new()
        self.ext_row.set_title(title=_("Extensions"))
        self.ext_row.set_use_markup(True)
        self.ext_row.set_title_lines(2)
        self.ext_row.set_subtitle_lines(3)
        self.ext_row.add_suffix(self.switch_ext)
        self.ext_row.set_activatable_widget(self.switch_ext)
        self.itemsBox.append(child=self.ext_row)
