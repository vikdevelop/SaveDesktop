import gi, sys, os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from pathlib import Path
from savedesktop.gui.custom_dirs_dialog import CustomDirsDialog
from savedesktop.gui.flatpak_apps_dialog import FolderSwitchRow, FlatpakAppsDialog
from savedesktop.core.synchronization_setup import create_savedesktop_json
from savedesktop.globals import *

class itemsDialog(Adw.AlertDialog):
    def __init__(self, parent, items_list=None):
        super().__init__()
        self.parent = parent
        self.items_list = items_list if items_list is not None else []

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
        if self.should_show("icon-themes.tgz", "icon-themes-legacy.tgz"):
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
        if self.should_show(".themes", "themes"):
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
        if self.should_show("fonts", ".fonts"):
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
        if self.should_show("backgrounds"):
            self.itemsBox.append(child=self.backgrounds_row)
        
        # show extension switch and row if user has installed these environments
        if environment["de_name"] in ["GNOME", "Cinnamon", "COSMIC (Old)", "KDE Plasma"]:
            self.show_extensions_row()
        
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
            if self.should_show("gtk-3.0"):
                self.itemsBox.append(child=self.gtk_row)

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
        if self.should_show("desktop-folder.tgz"):
            self.itemsBox.append(child=self.desktop_row)

        # Custom directories section
        self.custom_switch = Gtk.Switch.new()
        self.custom_switch.set_valign(Gtk.Align.CENTER)
        if settings["enable-custom-dirs"]:
            self.custom_switch.set_active(True)

        self.custom_button = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self.custom_button.add_css_class("flat")
        self.custom_button.set_valign(Gtk.Align.CENTER)
        self.custom_button.connect("clicked", self._show_custom_dirs_dialog)

        self.custom_row = Adw.ActionRow.new()
        self.custom_row.set_title(_("Custom folders"))
        self.custom_row.add_suffix(self.custom_switch)
        if self.custom_switch.get_active():
            self.custom_row.add_suffix(self.custom_button)
        if self.should_show("Custom_Dirs"):
            self.itemsBox.append(child=self.custom_row)

        self.custom_switch.connect('notify::active', self._set_show_custom_button)

        if flatpak and self.should_show("installed_flatpaks.sh"):
            self.flatpak_row = Adw.ExpanderRow.new()
            self.flatpak_row.set_title(title=_("Flatpak apps"))
            self.flatpak_row.set_subtitle(f"<a href='https://vikdevelop.github.io/SaveDesktop/wiki/flatpak_apps/{language}'>{_('Learn more')}</a>")
            self.flatpak_row.set_use_markup(True)
            self.flatpak_row.set_title_lines(2)
            self.flatpak_row.set_subtitle_lines(3)
            self.itemsBox.append(child=self.flatpak_row)
            
            # If it's available only one folder in the dir below, the row will not be displayed
            path = Path(f"{home}/.var/app")
            folders_dict = {f.name: str(f) for f in path.iterdir() if f.is_dir()}

            if len(folders_dict) > 1:
                self.appsButton = Gtk.Button.new_from_icon_name("go-next-symbolic")
                self.appsButton.add_css_class("flat")
                self.appsButton.set_valign(Gtk.Align.CENTER)
                self.appsButton.connect("clicked", self.manage_data_list)

                self.mngmt_row = Adw.ActionRow.new()
                self.mngmt_row.set_title(_("Select Flatpak apps"))
                self.mngmt_row.add_suffix(self.appsButton)
                self.mngmt_row.set_activatable_widget(self.appsButton)
                self.flatpak_row.add_row(self.mngmt_row)

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
            
            self.data_row = Adw.ActionRow.new()
            self.data_row.set_title(title=_("User data of installed Flatpak apps"))
            self.data_row.set_use_markup(True)
            self.data_row.set_title_lines(4)
            self.data_row.add_suffix(self.switch_06)
            self.data_row.set_activatable_widget(self.switch_06)
            self.flatpak_row.add_row(child=self.data_row)
            
            if settings["save-flatpak-data"]:
                self.switch_06.set_active(True)
            self.switch_06.set_valign(align=Gtk.Align.CENTER)

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

    def should_show(self, *search_terms):
        if not self.items_list:
            return True

        for term in search_terms:
            for item in self.items_list:
                if term in item:
                    return True

        return False

    def _set_show_custom_button(self, GParamBoolean, custom_switch):
        if self.custom_switch.get_active():
            self.custom_row.add_suffix(self.custom_button)
        else:
            self.custom_row.remove(self.custom_button)

    def _set_sw05_sensitivity(self, GParamBoolean, switch_05):
        if not self.switch_05.get_active():
            self.switch_06.set_sensitive(False)
            self.switch_06.set_active(False)
            self.switch_07.set_sensitive(False)
            self.switch_07.set_active(True)
        else:
            self.switch_06.set_sensitive(True)
            self.switch_07.set_sensitive(True)

    def _show_custom_dirs_dialog(self, w):
        self.CDDialog = CustomDirsDialog(self.parent)
        self.CDDialog.choose(self.parent, None, None, None)
        self.CDDialog.present(self.parent)

    # show dialog for managing Flatpak applications data
    def manage_data_list(self, w):
        self.appd = FlatpakAppsDialog(self.parent)
        self.appd.choose(self.parent, None, None, None)
        self.appd.present(self.parent)

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
        if self.should_show("cinnamon", "gnome-shell", "plasma"):
            self.itemsBox.append(child=self.ext_row)

    # Action after closing itemsDialog
    def itemsdialog_closed(self, w, response):
        if response == 'ok':
            # Saving the selected options to GSettings database
            settings["save-icons"] = self.switch_01.get_active()
            settings["save-themes"] = self.switch_02.get_active()
            settings["save-fonts"] = self.switch_03.get_active()
            settings["save-backgrounds"] = self.switch_04.get_active()
            settings["save-desktop-folder"] = self.switch_de.get_active()
            settings["enable-custom-dirs"] = self.custom_switch.get_active()
            if hasattr(self, "switch_gtk"):
                settings["save-bookmarks"] = self.switch_gtk.get_active()
            if settings["periodic-saving"] != "Never" and os.path.exists(f"{settings['periodic-saving-folder']}/SaveDesktop.json"):
                create_savedesktop_json()
            if flatpak:
                settings["save-installed-flatpaks"] = self.switch_05.get_active()
                settings["save-flatpak-data"] = self.switch_06.get_active()
                settings["keep-flatpaks"] = self.switch_07.get_active()
            if hasattr(self, "switch_ext"):
                settings["save-extensions"] = self.switch_ext.get_active()
