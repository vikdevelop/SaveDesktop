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

        self.subtitle = f'{_("Select custom folders and files to include in the configuration archive.")}'
        if flatpak:
            self.subtitle += f'\n{_("<i>Since you are using Flatpak, pay attention to the path format. <b>If the selected path begins at /run/user/</b>, it would be necessary to grant access to the folder you want to select.</i>")} <a href="https://linuxconfig.org/how-to-manage-flatpaks-privileges-with-flatseal">{_("Learn more")}</a>'

        self.set_heading(_("Custom folders and files"))
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
        self._show_add_section()

    def _activate_folders_list(self):
        # listbox for showing items
        self.flow_box = Gtk.ListBox.new()
        self.flow_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.flow_box.add_css_class(css_class='boxed-list')
        self.box.append(self.flow_box)

        self.add_response('ok', _("Apply"))
        self.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED)

    def _show_add_section(self):
        self.add_box = Gtk.ListBox.new()
        self.add_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.add_box.add_css_class(css_class='boxed-list')
        self.box.append(self.add_box)

        self.add_folder_button = Gtk.Button.new_from_icon_name("list-add-symbolic")
        self.add_folder_button.add_css_class("suggested-action")
        self.add_folder_button.add_css_class("circular")
        self.add_folder_button.set_valign(Gtk.Align.CENTER)
        self.add_folder_button.set_halign(Gtk.Align.CENTER)
        self.add_folder_button.connect("clicked", self._show_folders_dialog)

        self.add_folder_row = Adw.ActionRow.new()
        self.add_folder_row.set_title(_("Add folder"))
        self.add_folder_row.set_activatable_widget(self.add_folder_button)
        self.add_folder_row.add_suffix(self.add_folder_button)
        self.add_box.append(self.add_folder_row)

        self.add_file_button = Gtk.Button.new_from_icon_name("list-add-symbolic")
        self.add_file_button.add_css_class("circular")
        self.add_file_button.set_valign(Gtk.Align.CENTER)
        self.add_file_button.set_halign(Gtk.Align.CENTER)
        self.add_file_button.connect("clicked", self._show_files_dialog)

        self.add_file_row = Adw.ActionRow.new()
        self.add_file_row.set_title(_("Add file"))
        self.add_file_row.set_activatable_widget(self.add_file_button)
        self.add_file_row.add_suffix(self.add_file_button)
        self.add_box.append(self.add_file_row)

    def _show_folders_dialog(self, w):
        def set_selected(source, res, data):
            try:
                folder = source.select_folder_finish(res)
            except GLib.Error:
                return # User cancelled selection

            folder_path = folder.get_path()

            self._add_new_path(folder_path)

        self.file_chooser = Gtk.FileDialog.new()
        self.file_chooser.set_modal(True)
        self.file_chooser.set_title(_("Choose another folder"))
        self.file_chooser.select_folder(self.parent, None, set_selected, None)

    def _show_files_dialog(self, w):
        def set_selected(source, res, data):
            try:
                file = source.open_finish(res)
            except GLib.Error:
                return # User cancelled selection

            folder_path = file.get_path()

            self._add_new_path(folder_path)

        self.file_chooser = Gtk.FileDialog.new()
        self.file_chooser.set_modal(True)
        self.file_chooser.set_title(_("Choose another folder"))
        self.file_chooser.open(self.parent, None, set_selected, None)

    def _add_new_path(self, folder_path):
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
