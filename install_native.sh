#!/usr/bin/bash
#git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop
if [ "$1" == "--install" ]
then
		cd /tmp/SaveDesktop
		sed -i 's\Exec=run.sh\Exec=/usr/bin/savedesktop\' flatpak/io.github.vikdevelop.SaveDesktop.desktop
		sudo cp run_natively.sh /usr/bin/savedesktop
		sudo cp flatpak/io.github.vikdevelop.SaveDesktop.desktop /usr/share/applications/
		sudo cp flatpak/io.github.vikdevelop.SaveDesktop.metainfo.xml /usr/share/metainfo/
		sudo cp flatpak/io.github.vikdevelop.SaveDesktop.gschema.xml /usr/share/glib-2.0/schemas/
		sudo mkdir /usr/share/savedesktop
		sudo cp -R src /usr/share/savedesktop/
		sudo cp -R translations /usr/share/savedesktop/
		sudo install -D -t LICENSE /usr/share/licenses/savedesktop
		sudo glib-compile-schemas /usr/share/glib-2.0/schemas
		# Install app icons
		sudo install -D -t /usr/share/icons/hicolor/scalable/apps flatpak/icons/io.github.vikdevelop.SaveDesktop.svg
		sudo install -D -t /usr/share/icons/hicolor/symbolic/apps flatpak/icons/io.github.vikdevelop.SaveDesktop-symbolic.svg
		sudo install -D -t /usr/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/desktop-symbolic.svg
		cd
		rm -rf /tmp/SaveDesktop
elif [ "$1" == "--remove" ]
			then
					sudo rm /usr/bin/savedesktop/run_natively.sh
					sudo rm /usr/share/applications/io.github.vikdevelop.SaveDesktop.desktop
					sudo rm /usr/share/metainfo/io.github.vikdevelop.SaveDesktop.metainfo.xml
					sudo rm /usr/share/glib-2.0/schemas/io.github.vikdevelop.SaveDesktop.gschema.xml
					sudo rm -rf /usr/share/savedesktop
					sudo rm -rf LICENSE /usr/share/licenses/savedesktop
					# Install app icons
					sudo rm /usr/share/icons/hicolor/scalable/apps/io.github.vikdevelop.SaveDesktop.svg
					sudo rm /usr/share/icons/hicolor/symbolic/apps/io.github.vikdevelop.SaveDesktop-symbolic.svg
					sudo rm /usr/share/icons/hicolor/symbolic/apps/desktop-symbolic.svg
fi
