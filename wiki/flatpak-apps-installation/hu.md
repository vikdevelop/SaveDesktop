{% include head.html %}

# Telepített Flatpak alkalmazások mentése és listából telepítése
A 2.5-ös verzió óta a SaveDesktop lehetővé teszi a telepített Flatpak alkalmazások mentését és a listából történő telepítését. Hogyan is működik?

### A telepített Flatpak alkalmazások mentése
It is possible to save a list of installed Flatpak applications installed in the system directory /var/lib/flatpak/app and the home directory ~/.local/share/flatpak/app. The list of installed Flatpak applications in the configuration archive is marked as installed_flatpaks.sh for the system directory and installed_user_flatpaks.sh for the home directory.

### Flatpak alkalmazások telepítése a listából
A mentett konfigurációs fájl importálása és újbóli bejelentkezés után **a Flatpak alkalmazások telepítése megkezdődik a háttérben.**



{% include footer.html %}
