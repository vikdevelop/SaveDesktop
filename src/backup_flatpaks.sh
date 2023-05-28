flatpak-spawn --host flatpak list --app --columns=origin --columns=application | awk '{print "flatpak-spawn --host flatpak install " $1,$2 " -y"}' > ./installed_flatpaks.sh
