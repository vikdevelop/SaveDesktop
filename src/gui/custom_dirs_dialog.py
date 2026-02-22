import gi, sys, os, subprocess
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from savedesktop.globals import *

# dialog for showing custom dirs
class CustomDirsDialog(Adw.AlertDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.old_settings = settings["custom-dirs"]

        self.subtitle = f'{_("Select custom folders to include in the configuration archive.")}'
        if flatpak:
            self.subtitle += f'\n{_("<i>Since you are using Flatpak, pay attention to the path format. <b>If the selected path begins at /run/user/</b>, it would be necessary to grant access to the folder you want to select.</i>")} <a href="https://linuxconfig.org/how-to-manage-flatpaks-privileges-with-flatseal">{_("Learn more")}</a>'

        self.set_heading(_("Custom folders"))
        self.set_body(self.subtitle)
        self.set_body_use_markup(True)

        # add the Cancel button
        self.add_response('cancel', _("Cancel"))
        self.connect('response', self.apply_settings)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.set_extra_child(self.box)

        if not settings["custom-dirs"] == []:
            self._activate_folders_list()

        if settings["custom-dirs"]:
            self.load_folders()
        self._show_add_button()

    def _activate_folders_list(self):
        # listbox for showing items
        self.flow_box = Gtk.ListBox.new()
        self.flow_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.flow_box.add_css_class(css_class='boxed-list')
        self.box.append(self.flow_box)

        self.add_response('ok', _("Apply"))
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)

    def _show_add_button(self):
        self.button = Gtk.Button.new_with_label(_("Add folder"))
        self.button.add_css_class("suggested-action")
        self.button.add_css_class("pill")
        self.button.set_valign(Gtk.Align.CENTER)
        self.button.set_halign(Gtk.Align.CENTER)
        self.button.connect("clicked", self._show_file_dialog)
        self.box.append(self.button)

    def _show_file_dialog(self, w):
        def import_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except GLib.Error:
                return # User cancelled selection

            folder_path = folder.get_path()

            del_button = Gtk.Button.new_from_icon_name("user-trash-symbolic")
            del_button.add_css_class("destructive-action")
            del_button.set_tooltip_text(_("Remove"))
            del_button.set_valign(Gtk.Align.CENTER)
            del_button.connect("clicked", self._remove_folder)

            if "/run/user" in folder_path:
                folder_path = f"<span color='orange'>{folder_path}</span>"

            row = Adw.ActionRow.new()
            row.set_title(folder_path)
            row.set_use_markup(True)
            row.add_suffix(del_button)

            try:
                self.flow_box.append(row)
            except AttributeError:
                self._activate_folders_list()
                self.flow_box.append(row)
                self.box.remove(self.button)
                self.box.append(self.button)

        self.file_chooser = Gtk.FileDialog.new()
        self.file_chooser.set_modal(True)
        self.file_chooser.set_title(_("Choose another folder"))
        self.file_chooser.select_folder(self.parent, None, import_selected, None)

    def load_folders(self):
        while child := self.flow_box.get_first_child():
            self.flow_box.remove(child)

        folders = settings.get_strv("custom-dirs")
        for folder in folders:
            del_button = Gtk.Button.new_from_icon_name("user-trash-symbolic")
            del_button.add_css_class("destructive-action")
            del_button.set_tooltip_text(_("Remove"))
            del_button.set_valign(Gtk.Align.CENTER)

            del_button.connect("clicked", self._remove_folder)

            if "/run/user" in folder:
                folder = f"<span color='orange'>{folder}</span>"

            row = Adw.ActionRow.new()
            row.set_title(folder)
            row.set_use_markup(True)
            row.set_title_lines(4)
            row.add_suffix(del_button)

            self.flow_box.append(row)

    def _remove_folder(self, button):
        target = button
        while target is not None and not isinstance(target, Gtk.ListBoxRow):
            target = target.get_parent()

        if target:
            self.flow_box.remove(target)
        else:
            print("Error: Couldn't find the parent's Gtk.ListBoxRow")

    def apply_settings(self, w, response):
        if response == "ok":
            new_list = []

            child = self.flow_box.get_first_child()

            while child is not None:
                if isinstance(child, Adw.ActionRow):
                    title = child.get_title()
                    if title:
                        new_list.append(title)

                child = child.get_next_sibling()

            print(f"Saving custom-dirs: {new_list}")

            settings.set_strv("custom-dirs", new_list)

        elif response == "cancel":
            settings.set_strv("custom-dirs", self.old_settings)
