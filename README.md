<div align="center">
  <img src="/data/icons/hicolor/scalable/apps/io.github.vikdevelop.SaveDesktop.svg" width="128"/>
  <h1>Save Desktop</h1>
  <p><i>Save your desktop configuration</i></p>

  <a href='https://flathub.org/apps/io.github.vikdevelop.SaveDesktop'><img width='180' alt='Download on Flathub' src='https://flathub.org/api/badge?svg&locale=en&light'/></a>
  
  ![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)
  ![Translations](https://hosted.weblate.org/widget/vikdevelop/savedesktop/svg-badge.svg)
</div>

## 🚀 About

**Save Desktop** is a cross-desktop tool to **back up, restore and sync your entire Linux desktop setup**.  
It can save your themes, icons, fonts, settings, wallpapers (even dynamic ones), Flatpak apps and user data – and bring them back in just a few clicks.

## 📸 Screenshots

| Save Page | Import Page | Sync Page |
|-------------|-------------|-----------|
| ![Save Page dark](/data/screenshots/save_page_dark.png#gh-dark-mode-only) ![Save Page light](/data/screenshots/save_page.png#gh-light-mode-only)<br><sub>Save your setup</sub> | ![Import Page dark](/data/screenshots/import_page_dark.png#gh-dark-mode-only) ![Import Page light](/data/screenshots/import_page.png#gh-light-mode-only)<br><sub>Restore from backup</sub> | ![Sync Page dark](/data/screenshots/sync_page_dark.png#gh-dark-mode-only) ![Sync Page light](/data/screenshots/sync_page.png#gh-light-mode-only)<br><sub>Sync with other computers through the cloud</sub> |

## ✨ Features

- Backup your **icons, themes, fonts and wallpapers**
- Save **desktop settings** across environments
- Include **Flatpak apps and user data**
- Restore everything in one click
- Sync with cloud folders
- Works with **GNOME, KDE Plasma, Xfce, Cinnamon, Budgie, COSMIC, Pantheon, MATE, Deepin** and **Hyprland**

<details>
  <summary><b>Full list of supported desktops & directories</b></summary>

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
  - ~/.local/share/flatpak/app
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
  - ~/.config/budgie-extras
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
  - ~/.local/share/[k]* (all directories and files beginning with k)
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

## 📦 Installation

### Stable releases

> [!NOTE]
> **Flathub**: The latest stable releases (recommended)
> 
> <a href='https://flathub.org/apps/io.github.vikdevelop.SaveDesktop'><img width='180' alt='Download on Flathub' src='https://flathub.org/api/badge?svg&locale=en&light'/></a>

> [!IMPORTANT]
> **Snap Store**: Frozen at version `3.6.2-hotfix`, no updates will be provided. Active development continues on Flathub (see above).
>
> <a href="https://snapcraft.io/savedesktop"><img alt="Get it from the Snap Store" src="https://snapcraft.io/en/light/install.svg" /></a>

### Beta releases
- Flathub Beta:
  - [**Install from Flathub Beta**](https://dl.flathub.org/beta-repo/appstream/io.github.vikdevelop.SaveDesktop.flatpakref)

* GNOME Builder (for development):

  1. Install GNOME Builder from [Flathub](https://flathub.org/apps/org.gnome.Builder)
  2. Clone this repo and run the project

## 🤝 Contributing

I welcome contributions of all kinds!

* **Code** → see [CONTRIBUTING.md](https://github.com/vikdevelop/SaveDesktop/blob/main/CONTRIBUTING.md)
* **Translations** → contribute via Weblate:

  | App                                                                                                                                                                                      | Wiki                                                                                                                                                                                                             |
  | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | <a href="https://hosted.weblate.org/projects/vikdevelop/savedesktop/"><img src="https://hosted.weblate.org/widget/vikdevelop/savedesktop/287x66-grey.png" alt="Translation status"/></a> | <a href="https://hosted.weblate.org/projects/vikdevelop/savedesktop-github-wiki/"><img src="https://hosted.weblate.org/widget/vikdevelop/savedesktop-github-wiki/287x66-grey.png" alt="Translation status"/></a> |
* **Issues & bugs** → [GitHub Issues](https://github.com/vikdevelop/SaveDesktop/issues) or [Open issue without GitHub](https://vikdevelop.github.io/SaveDesktop/open-issue/)
* **Discussions** → [GitHub Discussions](https://github.com/vikdevelop/SaveDesktop/discussions)

This project follows the [GNOME Code of Conduct](https://conduct.gnome.org).

## 📜 License

Save Desktop is licensed under the [GPL-3.0 License](LICENSE).
