#!/usr/bin/python3
import os
from localization import home

if os.path.exists(f"{home}/.local/share/gnome-shell"):
    environment = 'GNOME'
elif os.path.exists(f"{home}/.config/pop-shell"):
    environment = 'COSMIC'
elif os.path.exists(f"{home}/.config/marlin"):
    environment = 'Pantheon'
elif os.path.exists(f"{home}/.local/share/cinnamon"):
    environment = 'Cinnamon'
elif os.path.exists(f"{home}/.config/nemo"):
    environment = 'Budgie'
elif os.path.exists(f"{home}/.config/xfce4"):
    environment = 'Xfce'
elif os.path.exists(f"{home}/.config/caja"):
    environment = 'MATE'
elif os.path.exists(f"{home}/.config/kdeglobals"):
    environment = 'KDE Plasma'
else:
    environment = None
