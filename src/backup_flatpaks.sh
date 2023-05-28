ls /var/lib/flatpak/app/ | awk '{print "flatpak install " $1 " -y"}' > ./installed_flatpaks.sh 
