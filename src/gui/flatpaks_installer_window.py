import sys, gi, threading, time, shutil, os, re
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
from savedesktop.globals import *

class FlatpaksWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(_("Installing your Flatpak apps..."))

        # header bar and toolbarview
        self.headerbar = Adw.HeaderBar.new()
        self.toolbarview = Adw.ToolbarView.new()
        self.toolbarview.add_top_bar(self.headerbar)
        self.set_content(self.toolbarview)

        self.set_size_request(360, 600)

        # primary layout
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled.set_vexpand(True)
        self.scrolled.set_hexpand(True)
        self.toolbarview.set_content(self.scrolled)

        self.winBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.winBox.set_valign(Gtk.Align.FILL)
        self.winBox.set_halign(Gtk.Align.FILL)
        self.winBox.set_vexpand(True)
        self.winBox.set_hexpand(True)
        self.scrolled.set_child(self.winBox)

        # Status page
        self.status_page = Adw.StatusPage.new()
        self.status_page.set_description(_("You can continue using your computer; everything runs in the background. Once the installation of your Flatpak apps and, if applicable, your user data is complete, a message will appear here and you’ll also see a system notification. You can also show the progress below."))
        self.winBox.append(self.status_page)

        self.progress_bar = Gtk.ProgressBar()
        # Add some margins so it doesn't touch the edges of the window
        self.progress_bar.set_margin_start(20)
        self.progress_bar.set_margin_end(20)
        self.progress_bar.set_margin_bottom(10)
        # Set initial state to 0%
        self.progress_bar.set_fraction(0.0)
        self.winBox.append(self.progress_bar)

        # Create TextView for logging
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

        # Wrapper ScrolledWindow for the logs
        self.log_scroller = Gtk.ScrolledWindow()
        self.log_scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.log_scroller.set_min_content_height(100)
        self.log_scroller.set_hexpand(True)
        self.log_scroller.set_vexpand(True)

        # Put the TextView inside this new ScrolledWindow
        self.log_scroller.set_child(self.text_view)

        # Append the ScrolledWindow to the main UI box
        self.winBox.append(self.log_scroller)

        thread = threading.Thread(target=self.read_pipe_background, daemon=True)
        thread.start()

    def read_pipe_background(self):
        log_path = os.path.expanduser(f"{CACHE}/workspace/log.pipe")
        print(f"[THREAD] Looking for log file at: {log_path}")

        # 1. Wait patiently until the logic script actually creates the file
        while not os.path.exists(log_path):
            print(f"[THREAD] Still waiting for {log_path} to exist...")
            time.sleep(0.5)

        print("[THREAD] File found! Opening it now...")

        # 2. Open the regular file ONCE and read it continuously
        try:
            with open(log_path, 'r') as log_file:
                while True:
                    line = log_file.readline()

                    if not line:
                        # Check if the host script finished and deleted the file
                        if not os.path.exists(log_path):
                            print("[THREAD] File was deleted. Killing thread cleanly.")
                            break # Kill the thread

                        # If file exists but no new data, chill for 100ms
                        time.sleep(0.1)
                        continue

                    # Send the new line to the main UI thread
                    GLib.idle_add(self.add_text_to_ui, line)

                    # 3. Explicit kill switch: FIXED TO MATCH YOUR REAL STRING
                    if "✔ All operations have been completed successfully." in line:
                        print("[THREAD] Success string found. Stopping background read.")
                        break

        except Exception as e:
            print(f"[THREAD] FATAL ERROR: {e}")

    def add_text_to_ui(self, text):
        print(f"DEBUG INCOMING: {text.strip()}")
        buffer = self.text_view.get_buffer()
        end_iter = buffer.get_end_iter()

        # 1. Full completion
        if "✔ All operations have been completed successfully." in text or "There's no need to install any new apps, since they're all available on your system." in text:
            self.progress_bar.set_fraction(1.0)
            self.send_completion_notification()
            cleanup_thread = threading.Thread(target=self.cache_cleanup)
            cleanup_thread.start()

        # 2. Pulse effect for ANY active operation
        if any(keyword in text for keyword in ["↓ Installing", "[COPY]", "[REMOVE]"]):
            self.progress_bar.pulse()

        # 3. Unified hidden progress tracker
        match = re.search(r"\[PROGRESS\] (\d+)/(\d+)", text)
        if match:
            try:
                current_step = int(match.group(1))
                total_steps = int(match.group(2))
                if total_steps > 0:
                    fraction = current_step / total_steps
                    self.progress_bar.set_fraction(fraction)
            except ValueError:
                pass

            # CRITICAL: We return False here immediately!
            # We DO NOT want to show the "[PROGRESS] 1/5" text in the UI log.
            return False

        # Insert normal text into the view
        buffer.insert(end_iter, text)

        # Autoscroll
        new_end_iter = buffer.get_end_iter()
        mark = buffer.create_mark(None, new_end_iter, False)
        self.text_view.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)
        buffer.delete_mark(mark)

        return False

    def send_completion_notification(self):
        # Create the notification object with a title
        notification = Gio.Notification.new(_("Your apps have been installed!"))

        # Optional: Set a system icon (or use your app's specific icon name)
        icon = Gio.ThemedIcon.new("object-select-symbolic")
        notification.set_icon(icon)

        # Get the application instance and send the notification
        # The string "install-complete" is just a unique ID for this specific notification
        app = self.get_application()
        if app:
            app.send_notification("install-complete", notification)

    def cache_cleanup(self):
        if os.path.exists(f"{CACHE}/workspace"):
            shutil.rmtree(f"{CACHE}/workspace")

        GLib.idle_add(self.start_auto_close_timer)

    def start_auto_close_timer(self):
        # 300 seconds = 2 minutes
        # GLib.timeout_add_seconds will wait in the background and then execute 'self.close_app'
        GLib.timeout_add_seconds(120, self.close_app)

        self.set_title(_("Your apps have been installed!"))
        self.status_page.set_icon_name("done")
        self.status_page.set_description(_("This window will be closed automatically in 2 minutes."))

        return False # Mandatory: tells idle_add to only run this setup once

    def close_app(self):
        # This is triggered when the 2 minutes are up.
        # Safely closes the current GTK window.
        self.close()

        return False # Mandatory: tells the timeout timer not to repeat itself

class FlatpaksInstallerApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE,
                         application_id="io.github.vikdevelop.SaveDesktop")
        self.connect('activate', self.on_activate)

    # Show the app window
    def on_activate(self, app):
        self.win = FlatpaksWindow(application=app)
        self.win.present()
