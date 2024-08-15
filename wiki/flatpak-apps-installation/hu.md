# Telepített Flatpak alkalmazások mentése és listából telepítése
A 2.5-ös verzió óta a SaveDesktop lehetővé teszi a telepített Flatpak alkalmazások mentését és a listából történő telepítését. Hogyan is működik?

### A telepített Flatpak alkalmazások mentése
It is possible to save a list of Flatpak applications installed in the system directory `/var/lib/flatpak/app`, and the home directory `~/.local/share/flatpak/app`. In the saved configuration archive, the list of installed Flatpak applications is labeled as `installedflatpaks.sh` (for home folder).

### Flatpak alkalmazások telepítése a listából
A mentett konfigurációs fájl importálása és újbóli bejelentkezés után **a Flatpak alkalmazások telepítése megkezdődik a háttérben.**



{% include footer.html %}
