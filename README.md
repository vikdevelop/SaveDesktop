
<p align="center">
  <img src="/flatpak/icons/io.github.vikdevelop.SaveDesktop.svg">
  <h1 align="center">SaveDesktop</h1>
  <p align="center">Save your desktop configuration</p>
</p>

![Main Window](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/save_page_dark.png#gh-dark-mode-only)
![Main Window](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/save_page.png#gh-light-mode-only)

![Import page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/import_page_dark.png#gh-dark-mode-only)
![Import page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/import_page.png#gh-light-mode-only)

![Sync page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/sync_page_dark.png#gh-dark-mode-only)
![Sync page](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/flatpak/screenshots/sync_page.png#gh-light-mode-only)

<br>

# Content
- [About](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#about)
    - [Supported environments](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#supported-environments)
    - [SaveDesktop features](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#savedesktop-can-save)
- [Contributing](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#contributing)
  - [Translations](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#translations)
  - [Reporting issues](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#reporting-issues)
- [Installation](https://github.com/vikdevelop/SaveDesktop?tab=readme-ov-file#installation)

## About
### Supported environments:
- GNOME
- Xfce
- Cinnamon
- Budgie
- COSMIC (Rust and GNOME version)
- Pantheon
- MATE
- KDE Plasma
- Deepin
- Hyprland (logging out of the system doesn't work yet)

### SaveDesktop can save:
- your icons, fonts, and themes
- your settings
- your backgrounds (including dynamic wallpapers, provided that the same username is retained)
- your installed Flatpak apps and their data
- your Desktop folder in the home directory
- other items related to your desktop environment (e.g., Cinnamon extensions and applets, KDE Plasma widgets, GNOME and Nautilus extensions, etc.)

NOTE: It can happen that a backup file will not be created, in that case, just allow access to the folder in the [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) app.

<details>
  <summary><b>Configuration directories that will be included in the archive</b></summary>
  
  - **General directories**
  ```
  - ~/.config/dconf
  - ~/.local/share/backgrounds 
  - ~/.themes
  - ~/.icons
  - ~/.local/share/icons
  - ~/.local/share/fonts
  - ~/.fonts
  - ~/.config/gtk-4.0 
  - ~/.config/gtk-3.0
  - ~/.var/app
  - /var/lib/flatpak/app
  ```
  - **GNOME**
  ```
   - ~/.local/share/gnome-background-properties
   - ~/.local/share/gnome-shell
   - ~/.local/share/nautilus-python
   - ~/.local/share/nautilus
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
  - **Cosmic (Old)**
  ```
  - ~/.config/pop-shell
  - ~/.local/share/gnome-shell
  ```
  - **Cosmic (New)**
  ```
  - ~/.config/cosmic
  - ~/.local/state/cosmic
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
  - **Deepin**
  ```
  - ~/.config/deepin
  - ~/.local/share/deepin
  ```
  - **Hyprland**
  ```
  - ~/.config/hypr
  ```
  
</details>

## Contributing
*See to the [CONTRIBUTING.md](https://github.com/vikdevelop/SaveDesktop/blob/main/CONTRIBUTING.md) for more information.*

### Translations
If you want to help localize SaveDesktop, you can use the Weblate tool (it is possible to register with, e.g., GitHub or Google).
| <h4>SaveDesktop application</h4> (click on widget below) | <h4>SaveDesktop Github wiki</h4> (click on widget below) |
| --- | --- |
| <a href="https://hosted.weblate.org/projects/vikdevelop/savedesktop/"><img src="https://hosted.weblate.org/widget/vikdevelop/savedesktop/287x66-grey.png" alt="Stav překladu" /></a> | <a href="https://hosted.weblate.org/projects/vikdevelop/savedesktop-github-wiki/"><img src="https://hosted.weblate.org/widget/vikdevelop/savedesktop-github-wiki/287x66-grey.png" alt="Stav překladu" title="For the language to be added to the Github Wiki, it should have translated at least seven of the 12 strings." /></a> |

### Reporting issues
You can report an issue on GitHub, or if you are not registered on GitHub, you can use this [web page](https://vikdevelop.github.io/SaveDesktop/open-issue/). You can also use [Github Discussions](https://github.com/vikdevelop/SaveDesktop/discussions).

## Installation
### Stable releases
- Flathub
  
  <a href='https://beta.flathub.org/apps/io.github.vikdevelop.SaveDesktop'><img width='240' alt='Download on Flathub' src='https://flathub.org/api/badge?locale=en'/></a>

- Snap

  <a href="https://snapcraft.io/savedesktop"><img alt="Get it from the Snap Store" src="https://snapcraft.io/static/images/badges/en/snap-store-black.svg" width='240' />
  </a>

- Install on the system (native version)
  
  ```bash
  # Install
  wget -qO /tmp/savedesktop-native-installer.py https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/native_installer.py && python3 /tmp/savedesktop-native-installer.py --install

  # Remove
  wget -qO /tmp/savedesktop-native-installer.py https://raw.githubusercontent.com/vikdevelop/SaveDesktop/main/native/native_installer.py && python3 /tmp/savedesktop-native-installer.py --remove
  ```
  **NOTE**: *For this installation method, you need to have GTK4 (v4.14) and LibAdwaita (v1.5) installed. To check versions of these libraries, you can use this command:*
  ```bash
  python3 -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1');from gi.repository import Gtk, Adw; print(f'GTK version: {Gtk.MAJOR_VERSION}.{Gtk.MINOR_VERSION}'); print(f'LibAdwaita version: {Adw.MAJOR_VERSION}.{Adw.MINOR_VERSION}')"
  ```

### Beta releases
If you want to help with the testing of the future releases of this app, you can use one of these options:

#### 1. Flathub Beta
Add the Flathub Beta repository to your system:
```
flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo
```
Install the SaveDesktop Beta from this repository:

```
flatpak install flathub-beta io.github.vikdevelop.SaveDesktop
```
#### 2. Snap
To install the SaveDesktop Beta, run the following command:
```
snap install savedesktop --beta
```
#### 3. Flatpak Builder
Before building this app using Flatpak Builder, ensure if you have installed org.gnome.Sdk runtime. If not, use this command: `flatpak install org.gnome.Sdk//47`

Then, you can continue in building this app using Flatpak Builder by entering this command:

```
git clone https://github.com/vikdevelop/SaveDesktop && cd SaveDesktop && flatpak-builder build *.yaml --install --user
```
