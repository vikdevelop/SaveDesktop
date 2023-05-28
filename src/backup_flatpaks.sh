ls /var/lib/flatpak/app/ | awk '{print "flatpak install --system " $1 " -y"}' > ./installed_flatpaks.sh 
