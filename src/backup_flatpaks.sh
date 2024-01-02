ls /var/lib/flatpak/app/ | awk '{print "flatpak install --system " $1 " -y"}' > ./installed_flatpaks.sh
ls ~/.local/share/flatpak/app | awk '{print "flatpak install --user " $1 " -y"}' > ./installed_user_flatpaks.sh
