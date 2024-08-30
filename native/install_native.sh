#!/usr/bin/bash
if [ "$1" = "--install" ]
then
		sed -i "s\Exec=run.sh\Exec=/home/${USER}/.local/bin/savedesktop\ " flatpak/io.github.vikdevelop.SaveDesktop.desktop
		install -Dm755 savedesktop ~/.local/bin/
		install -D -t ~/.local/share/applications flatpak/io.github.vikdevelop.SaveDesktop.desktop
		install -D -t ~/.local/share/metainfo flatpak/io.github.vikdevelop.SaveDesktop.metainfo.xml
		install -D -t ~/.local/share/glib-2.0/schemas flatpak/io.github.vikdevelop.SaveDesktop.gschema.xml
		mkdir ~/.local/share/savedesktop
		cp -R src ~/.local/share/savedesktop/
		cp -R translations ~/.local/share/savedesktop/
		install -D -t ~/.local/share/share/licenses/savedesktop LICENSE
  		install -D -t ~/.local/bin native/native_updater.py
    		echo -e "[Desktop Entry]\nName=SaveDesktop Native Updater\nType=Application\nExec=savedesktop --update" > ~/.config/autostart/io.github.vikdevelop.SaveDesktop.Updater.desktop
		export GSETTINGS_SCHEMA_DIR="~/.local/share/glib-2.0/schemas:${GSETTINGS_SCHEMA_DIR}"
		glib-compile-schemas ~/.local/share/glib-2.0/schemas
		# Install app icons
		install -D -t ~/.local/share/icons/hicolor/scalable/apps flatpak/icons/io.github.vikdevelop.SaveDesktop.svg
		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/icons/io.github.vikdevelop.SaveDesktop-symbolic.svg
		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/desktop-symbolic.svg
		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/list-view.png
  		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/done.svg
    		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/preferences-system-symbolic.svg
		# Create cache and data dirs
		mkdir ~/.cache/io.github.vikdevelop.SaveDesktop
		mkdir ~/.local/share/io.github.vikdevelop.SaveDesktop
		cd
		echo "SaveDesktop has been installed! You can run it with this command: \"savedesktop\" or \"~/.local/bin/savedesktop\"."
fi
if [ "$1" = "--remove" ]
			then
					rm ~/.local/bin/savedesktop
					rm ~/.local/share/applications/io.github.vikdevelop.SaveDesktop.desktop
					rm ~/.local/share/metainfo/io.github.vikdevelop.SaveDesktop.metainfo.xml
					rm ~/.local/share/glib-2.0/schemas/io.github.vikdevelop.SaveDesktop.gschema.xml
					rm -rf ~/.local/share/savedesktop
					rm -rf LICENSE ~/.local/share/licenses/savedesktop
					# Remove app icons
					rm ~/.local/share/icons/hicolor/scalable/apps/io.github.vikdevelop.SaveDesktop.svg
					rm ~/.local/share/icons/hicolor/symbolic/apps/io.github.vikdevelop.SaveDesktop-symbolic.svg
					rm ~/.local/share/icons/hicolor/symbolic/apps/desktop-symbolic.svg
					rm ~/.local/share/icons/hicolor/symbolic/apps/edit-symbolic.svg
					rm ~/.local/share/icons/hicolor/symbolic/apps/list-view.png
     					rm ~/.local/share/icons/hicolor/symbolic/apps/done.svg
	  				rm ~/.local/share/icons/hicolor/symbolic/apps/preferences-system-symbolic.svg
					rm -rf /tmp/SaveDesktop
					echo "SaveDesktop has been removed."
fi
