#!/usr/bin/bash
if [ "$1" == "--install" ]
then
		cd /tmp/SaveDesktop
		sed -i 's\Exec=run.sh\Exec=~/.local/bin/savedesktop\' flatpak/io.github.vikdevelop.SaveDesktop.desktop
		install -Dm755 run_natively.sh ~/.local/bin/savedesktop
		install -D -t ~/.local/share/applications flatpak/io.github.vikdevelop.SaveDesktop.desktop
		install -D -t ~/.local/share/metainfo flatpak/io.github.vikdevelop.SaveDesktop.metainfo.xml
		install -D -t ~/.local/share/glib-2.0/schemas flatpak/io.github.vikdevelop.SaveDesktop.gschema.xml
		mkdir ~/.local/share/savedesktop
		cp -R src ~/.local/share/savedesktop/
		cp -R translations ~/.local/share/savedesktop/
		install -D -t ~/.local/share/share/licenses/savedesktop LICENSE
		export GSETTINGS_SCHEMA_DIR="~/.local/share/glib-2.0/schemas:${GSETTINGS_SCHEMA_DIR}"
		glib-compile-schemas ~/.local/share/glib-2.0/schemas
		# Install app icons
		install -D -t ~/.local/share/icons/hicolor/scalable/apps flatpak/icons/io.github.vikdevelop.SaveDesktop.svg
		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/icons/io.github.vikdevelop.SaveDesktop-symbolic.svg
		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/desktop-symbolic.svg
		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/edit-symbolic.svg
		install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/list-view.png
		# Create cache and data dirs
		mkdir ~/.cache/io.github.vikdevelop.SaveDesktop
		mkdir ~/.local/share/io.github.vikdevelop.SaveDesktop
		cd
		rm -rf /tmp/SaveDesktop
		echo "SaveDesktop has been installed! You can run it with this command: \"savedesktop\" or \"~/.local/bin/savedesktop\"."
elif [ "$1" == "--remove" ]
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
					echo "SaveDesktop has been removed."
fi
