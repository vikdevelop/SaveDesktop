#!/usr/bin/bash
#git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop
cd /tmp/SaveDesktop
# Install app icons
install -D -t ~/.local/share/icons/hicolor/scalable/apps flatpak/icons/io.github.vikdevelop.SaveDesktop.svg
install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/icons/io.github.vikdevelop.SaveDesktop-symbolic.svg
if [ "$1" == "" ]
then 
	python3 src/main_window.py
elif [ "$1" == "--background" ]
	then
		echo "Periodic saving is currently only supported in Flatpak."
fi

cd
rm -rf /tmp/SaveDesktop
