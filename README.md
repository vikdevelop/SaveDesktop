
<p align="center">
  <img src="/flatpak/icons/io.github.vikdevelop.SaveDesktop.svg">
  <h1 align="center">SaveDesktop</h1>
  <p align="center">Save the current configuration of your desktop environment</p>
</p>

![Main Window](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/main_window_dark.png#gh-dark-mode-only)
![Main Window](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/main_window.png#gh-light-mode-only)

![Import page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/import_page_dark.png#gh-dark-mode-only)
![Import page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/import_page.png#gh-light-mode-only)

![Sync page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/sync_page_dark.png#gh-dark-mode-only)
![Sync page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/sync_page.png#gh-light-mode-only)

<br>

# Content
- [About](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#about)
    - [Supported environments](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#supported-environments)
    - [SaveDesktop can save](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#savedesktop-can-save)
    - [Translations](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#translations)
    - [Sending issues](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#sending-issues)
    - [Installation](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#installation)

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
- your icons, fonts, and themes
- your settings
- your backgrounds (including dynamic wallpapers, provided that the same username is retained)
- your GNOME and Nautilus extensions
- your installed Flatpak apps
- other items related to your desktop environment (e.g., Cinnamon extensions and applets, KDE Plasma widgets, etc.)

NOTE: It can happen that a backup file will not be created, in that case, just allow access to the folder in the [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) app.

<details>
  <summary><b>Configuration directories that will be included in the archive</b></summary>
  
  - **General directories**
  ```
  - ~/.config/dconf/user
  - ~/.local/share/backgrounds 
  - ~/.themes
  - ~/.icons
  - ~/.local/share/icons 
  - ~/.fonts
  - ~/.config/gtk-4.0 
  - ~/.config/gtk-3.0 
  ```
  - **GNOME**
  ```
   - ~/.local/share/gnome-background-properties
   - ~/.local/share/gnome-shell
   - ~/.local/share/nautilus-python
   - ~/.local/share/gnome-control-center
  ```
  - **Pantheon**
  ```
  - ~/.config/plank 
  - ~/.config/marlin 
  ```
  - **Cinnamon**
  ```
  - ~/.config/nemo
  - ~/.local/share/cinnamon
  - ~/.cinnamon
  ```
  - **Budgie**
  ```
  - ~/.config/budgie-desktop
  - ~/.config/bugie-extras
  - ~/.config/nemo
  ```
  - **Cosmic**
  ```
  - ~/.config/pop-shell
  - ~/.local/share/gnome-shell
  ```
  - **Xfce**
  ```
  - ~/.config/xfce4
  - ~/.config/Thunar
  - ~/.xfce4
  ```
  - **MATE**
  ```
  - ~/.config/caja
  ```
  - **KDE Plasma**
  ```
  - ~/.config/[k]* (all directories and files beginning with k)
  - ~/.config/gtkrc
  - ~/.config/dolphinrc
  - ~/.config/gwenviewrc
  - ~/.config/plasmashellrc
  - ~/.config/spectaclerc
  - ~/.config/plasmarc
  - ~/.config/plasma-org.kde.plasma.desktop-appletsrc
  - ~/.local/share/konsole
  - ~/.local/share/dolphin
  - ~/.local/share/sddm
  - ~/.local/share/wallpapers
  - ~/.local/share/plasma-systemmonitor
  - ~/.local/share/plasma
  - ~/.local/share/aurorae
  - ~/.local/share/kscreen
  - ~/.local/share/color-schemes
  ```
  
  
</details>

## Translations
If you want to help localize SaveDesktop, you can use the Weblate tool (it is possible to register with, e.g., GitHub or Google).
| <h4>SaveDesktop application</h4> (click on widget below) | <h4>SaveDesktop Github wiki</h4> (click on widget below) |
| --- | --- |
| <a href="https://hosted.weblate.org/projects/vikdevelop/savedesktop/"><img src="https://hosted.weblate.org/widget/vikdevelop/savedesktop/287x66-grey.png" alt="Stav překladu" /></a> | <a href="https://hosted.weblate.org/projects/vikdevelop/savedesktop-github-wiki/"><img src="https://hosted.weblate.org/widget/vikdevelop/savedesktop-github-wiki/287x66-grey.png" alt="Stav překladu" title="For the language to be added to the Github Wiki, it should have translated at least seven of the 12 strings." /></a> |

## Sending issues
You can send an issue on GitHub, or if you are not registered on GitHub, you can use this [web page](https://vikdevelop.github.io/SaveDesktop/open-issue/).

## Installation
- Flathub (stable version)
  
  <a href='https://beta.flathub.org/apps/io.github.vikdevelop.SaveDesktop'><img width='240' alt='Download on Flathub' src='https://dl.flathub.org/assets/badges/flathub-badge-en.png'/></a>

- Install on the system (native version)
  
  ```bash
  # Install
  wget -qO /tmp/savedesktop-native-installer.py https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/native_installer.py && python3 /tmp/savedesktop-native-installer.py --install
  # Remove
  wget -qO /tmp/savedesktop-native-installer.py https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/native_installer.py && python3 /tmp/savedesktop-native-installer.py --remove
  ```
  NOTE: For this installation method you need to have GTK4 (v4.10) and LibAdwaita (v1.3) installed.
  
- Build with Flatpak builder (beta version) ⚠️**UNSTABLE**⚠️
  ```
  git clone https://github.com/vikdevelop/SaveDesktop && cd SaveDesktop && flatpak-builder build *.yaml --install --user
  # Maybe you will need to install org.gnome.Sdk (version 44) with flatpak
  ```
