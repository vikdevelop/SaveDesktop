#!/usr/bin/bash

if [ "$1" = "--install" ]; then
    # Create cache and data dirs
    mkdir -p ~/.cache/io.github.vikdevelop.SaveDesktop
    mkdir -p ~/.local/share/io.github.vikdevelop.SaveDesktop
    install -Dm755 -t ~/.local/bin savedesktop
    install -D -t ~/.local/share/applications flatpak/io.github.vikdevelop.SaveDesktop.desktop
    install -D -t ~/.local/share/metainfo flatpak/io.github.vikdevelop.SaveDesktop.metainfo.xml
    install -D -t ~/.local/share/glib-2.0/schemas flatpak/io.github.vikdevelop.SaveDesktop.gschema.xml
    install -D -t ~/.local/share/licenses/savedesktop LICENSE
    mkdir -p ~/.local/share/savedesktop
    cp -R src ~/.local/share/savedesktop/
    cp -R translations ~/.local/share/savedesktop/
    cp -R native/native_installer.py ~/.local/share/savedesktop/
    echo -e "[Desktop Entry]\nName=SaveDesktop Native Updater\nType=Application\nExec=python3 ${HOME}/.local/share/savedesktop/native_installer.py --update" > ~/.config/autostart/io.github.vikdevelop.SaveDesktop.Updater.desktop
    export GSETTINGS_SCHEMA_DIR="$HOME/.local/share/glib-2.0/schemas:${GSETTINGS_SCHEMA_DIR}"
    glib-compile-schemas ~/.local/share/glib-2.0/schemas
    # Install app icons
    install -D -t ~/.local/share/icons/hicolor/scalable/apps flatpak/icons/io.github.vikdevelop.SaveDesktop.svg
    install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/icons/io.github.vikdevelop.SaveDesktop-symbolic.svg
    install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/desktop-symbolic.svg
    install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/list-view.png
    install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/done.svg
    install -D -t ~/.local/share/icons/hicolor/symbolic/apps flatpak/symbolic-icons/exclamation_mark.png
    cd
    echo "SaveDesktop has been installed! You can run it with this command: \"savedesktop\" or \"~/.local/bin/savedesktop\"."
fi

if [ "$1" = "--remove" ]; then
    rm ~/.local/bin/savedesktop
    rm ~/.local/share/applications/io.github.vikdevelop.SaveDesktop.desktop
    rm ~/.local/share/metainfo/io.github.vikdevelop.SaveDesktop.metainfo.xml
    rm ~/.local/share/glib-2.0/schemas/io.github.vikdevelop.SaveDesktop.gschema.xml
    rm -rf ~/.local/share/savedesktop
    rm -rf ~/.local/share/licenses/savedesktop
    # Remove app icons
    rm ~/.local/share/icons/hicolor/scalable/apps/io.github.vikdevelop.SaveDesktop.svg
    rm ~/.local/share/icons/hicolor/symbolic/apps/io.github.vikdevelop.SaveDesktop-symbolic.svg
    rm ~/.local/share/icons/hicolor/symbolic/apps/desktop-symbolic.svg
    rm ~/.local/share/icons/hicolor/symbolic/apps/list-view.png
    rm ~/.local/share/icons/hicolor/symbolic/apps/done.svg
    rm ~/.local/share/icons/hicolor/symbolic/apps/exclamation_mark.png
    cd
    echo "SaveDesktop has been removed."
fi
