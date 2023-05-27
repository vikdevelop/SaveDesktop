#!/usr/bin/bash
#git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop
cd /tmp/SaveDesktop
# Build GLib schema
mkdir ./glib-2.0/schemas
if test -f "/usr/share/glib-2.0/schemas/io.github.vikdevelop.SaveDesktop.gschema.xml"; then
	echo "-"
else
	echo "Please enter password, because it is neccessary for installing GLib schema."
	sudo cp flatpak/io.github.vikdevelop.SaveDesktop.gschema.xml /usr/share/glib-2.0/schemas/
	sudo glib-compile-schemas /usr/share/glib-2.0/schemas
fi
# Install app icons
install -D -t ~/.local/share/icons/hicolor/scalable/apps flatpak/icons/io.github.vikdevelop.SaveDesktop.svg
install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/icons/io.github.vikdevelop.SaveDesktop-symbolic.svg
install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/desktop-symbolic.svg
if [ "$1" == "" ]
then 
	python3 src/main_window.py
elif [ "$1" == "--background" ]
	then
		echo "Periodic saving is currently only supported in Flatpak."
fi

cd
rm -rf /tmp/SaveDesktop
