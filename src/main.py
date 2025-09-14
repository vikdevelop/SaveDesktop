import os, sys, gi, subprocess
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from threading import Thread
from savedesktop.gui.window import MainWindow
from savedesktop.globals import *

@Gtk.Template(resource_path="/io/github/vikdevelop/SaveDesktop/gui/templates/shortcuts_window.ui")
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'SaveDesktopShortcutsWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SaveDesktopApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE,
                         application_id="io.github.vikdevelop.SaveDesktop" if not snap else None)
        self.create_action('m-sync-with-key', self.sync_pc, ["<primary><shift>s"] if settings["manually-sync"] else None)
        self.create_action('save-config', self.call_saving_config, ["<primary>s"])
        self.create_action('import-config', self.call_importing_config, ["<primary>o"])
        self.create_action('ms-dialog', self.call_ms_dialog, ["<primary><shift>m"])
        self.create_action('items-dialog', self.call_items_dialog, ["<primary><shift>i"])
        self.create_action('set-dialog', self.call_setDialog, ["<primary><shift>f"])
        self.create_action('cloud-dialog', self.call_cloudDialog, ["<primary><shift>c"])
        self.create_action('open-wiki', self.open_wiki, ["F1"])
        self.create_action('quit', self.app_quit, ["<primary>q", "<primary>w"])
        self.create_action('shortcuts', self.shortcuts, ["<primary>question"])
        self.create_action('logout', self.logout)
        self.create_action('open_dir', self.open_dir)
        self.create_action('about', self.on_about_action)
        self.connect('activate', self.on_activate)

    # Synchronize configuation manually after clicking on the "Synchronise manually" button in the header bar menu
    def sync_pc(self, action, param):
        self.win.import_file = settings["file-for-syncing"]
        self.win.please_wait_import()
        sync_thread = Thread(target=self._sync_process)
        sync_thread.start()

    def _sync_process(self):
        try:
            os.system(f'notify-send "{_("Please wait …")}"')
            os.system(f"echo > {CACHE}/.from_app")
            subprocess.run([sys.executable, "-m", "savedesktop.core.synchronization"], check=True, env={**os.environ, "PYTHONPATH": f"{app_prefix}"})
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.win.show_err_msg, e)
            self.toolbarview.set_content(self.headapp)
            self.headerbar.set_title_widget(self.switcher_title)
            self.switcher_bar.set_reveal(self.switcher_title.get_title_visible())
        finally:
            self.win.applying_done()

    # Start saving the configuration using Ctrl+S keyboard shortcut
    def call_saving_config(self, action, param):
        self.win.select_folder(w="")

    # Start importing the configuration using Ctrl+I keyboard shortcut
    def call_importing_config(self, action, param):
        self.win.select_file_to_import(w="")

    # Open the More options dialog using Ctrl+Shift+M keyboard shortcut
    def call_ms_dialog(self, action, param):
        self.win._open_more_options_dialog(w="")

    # Open the "Items to include in the configuration archive" dialog using Ctrl+Shift+I keyboard shortcut
    def call_items_dialog(self, action, param):
        self.win._open_itemsDialog(w="")

    # Open the "Set up the sync file" dialog using Ctrl+Shift+S keyboard shortcut
    def call_setDialog(self, action, param):
        if not snap:
            self.win._open_SetDialog(w="set-button") if not settings["first-synchronization-setup"] else self.win._open_InitSetupDialog(w="set-button")

    # Open the "Connect to the cloud drive" dialog using Ctrl+Shift+C keyboard shortcut
    def call_cloudDialog(self, action, param):
        if not snap:
            self.win._open_CloudDialog(w="get-button") if not settings["first-synchronization-setup"] else self.win._open_InitSetupDialog(w="get-button")

    # Open the application wiki using F1 keyboard shortcut
    def open_wiki(self, action, param):
        os.system("xdg-open https://vikdevelop.github.io/SaveDesktop/wiki")

    # Action after closing the application using Ctrl+Q keyboard shortcut
    def app_quit(self, action, param):
        self.win.on_close(w="")
        self.quit()

    # Show Keyboard Shortcuts window
    def shortcuts(self, action, param):
        ShortcutsWindow(transient_for=self.get_active_window()).present()

    # log out of the system after clicking on the "Log Out" button
    def logout(self, action, param):
        if snap:
            os.system("dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 org.freedesktop.login1.Manager.TerminateSession string:$(dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 org.freedesktop.login1.Manager.ListSessions | awk -F 'string \"' '/string \"/ {print $2; exit}' | awk -F '\"' '{print $1}')")
        else:
            if self.win.environment == 'Xfce':
                os.system("dbus-send --print-reply --session --dest=org.xfce.SessionManager /org/xfce/SessionManager org.xfce.Session.Manager.Logout boolean:true boolean:false")
            elif self.win.environment == 'KDE Plasma':
                os.system("dbus-send --print-reply --session --dest=org.kde.LogoutPrompt /LogoutPrompt org.kde.LogoutPrompt.promptLogout")
            elif self.win.environment == 'COSMIC (New)':
                os.system("dbus-send --print-reply --session --dest=com.system76.CosmicSession --type=method_call /com/system76/CosmicSession com.system76.CosmicSession.Exit")
            elif self.win.environment == 'Hyprland':
                os.system("hyprctl dispatch exit")
            else:
                os.system("gdbus call --session --dest org.gnome.SessionManager --object-path /org/gnome/SessionManager --method org.gnome.SessionManager.Logout 1")

    # open a directory with created configuration archive after clicking on the "Open the folder" button
    def open_dir(self, action, param):
        if settings["save-without-archive"]:
            path = f"{self.win.folder}/{self.win.filename_text}"
        else:
            path = f"{self.win.folder}/{self.win.filename_text}.sd.zip"

        Gtk.FileLauncher.new(Gio.File.new_for_path(path)).open_containing_folder()

    # "About app" dialog
    def on_about_action(self, action, param):
        app_version = os.environ.get("SAVEDESKTOP_VERSION")
        dialog = Adw.AboutDialog(
            application_name="Save Desktop",
            developer_name="vikdevelop",
            comments=_("Save your desktop configuration"),
            license_type=Gtk.License.GPL_3_0,
            website="https://vikdevelop.github.io/SaveDesktop",
            issue_url="https://github.com/vikdevelop/SaveDesktop/issues",
            copyright="© 2023-2025 vikdevelop",
            developers=["vikdevelop https://github.com/vikdevelop"],
            artists=["Brage Fuglseth"],
            version=app_version,
            application_icon="io.github.vikdevelop.SaveDesktop",
            release_notes=f"<p>https://github.com/vikdevelop/SaveDesktop/releases/tag/{app_version}</p>",
        )

        if _("Translator credits") != "Translator credits":
            dialog.set_translator_credits(_("Translator credits"))

        dialog.present(app.get_active_window())

    # create Gio actions for opening the folder, logging out of the system, etc.
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)

    # Show the main window of the application
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = SaveDesktopApp()
app.run(sys.argv)
