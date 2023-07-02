<p align="center">
  <img src="/flatpak/icons/io.github.vikdevelop.SaveDesktop.svg">
  <h1 align="center">SaveDesktop</h1>
  <p align="center">Save the current configuration of your desktop environment</p>
</p>

<br>

## Installation
- Flathub (stable version)
  
  <a href='https://beta.flathub.org/apps/io.github.vikdevelop.SaveDesktop'><img width='240' alt='Download on Flathub' src='https://dl.flathub.org/assets/badges/flathub-badge-en.png'/></a>

- Install to system (native version)
  
  ```bash
  # Install
  git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop && sh /tmp/SaveDesktop/install_native.sh --install
  # Remove
  git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop && sh /tmp/SaveDesktop/install_native.sh --remove
  ```
  NOTE: For this installation method you need to have GTK4 (v4.10) and LibAdwaita (v1.3) installed.
- Build with Flatpak builder (beta version)
  ```
  git clone https://github.com/vikdevelop/SaveDesktop && cd SaveDesktop && flatpak-builder build *.yaml --install --user
  # Maybe you will need to install org.gnome.Sdk (version 44) with flatpak
  ```

## Translations
If you want to help with localize SaveDesktop, you can use the Weblate tool (is possible register with e.g. GitHub or Google)

<a href="https://hosted.weblate.org/projects/vikdevelop/savedesktop/">
<img src="https://hosted.weblate.org/widgets/vikdevelop/-/savedesktop/open-graph.png" alt="Stav překladu" width=300 />
</a>

## About
### Supported environments:
- GNOME
- Xfce
- Cinnamon
- Budgie
- COSMIC (Pop!_OS)
- Pantheon
- MATE
- KDE Plasma

### SaveDesktop can save:
- your icons, fonts and themes
- your settings
- your backgrounds (including dynamic wallpapers, provided that the same username is retained)
- your GNOME and Nautilus extensions
- your installed Flatpak apps

and more...

### Screenshots
![Main Window](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/main_window_dark.png#gh-dark-mode-only)
![Main Window](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/main_window.png#gh-light-mode-only)

![Import page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/import_page_dark.png#gh-dark-mode-only)
![Import page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/import_page.png#gh-light-mode-only)
