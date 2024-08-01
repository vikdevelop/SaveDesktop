# Desa el programari Flatpak per ser instal·lat des d'una llista
Des de la versió 2.5, el SaveDesktop us permet desar el programari Flatpak existent i instal·lar-ho des d'una llista. Com funciona això?

### Desat del programari Flatpak instal·lat
It is possible to save a list of Flatpak applications installed in the system directory `/var/lib/flatpak/app`, and the home directory `~/.local/share/flatpak/app`. In the saved configuration archive, the list of installed Flatpak applications is labeled as `installed_flatpaks.sh` (for system directory) and `installed_user_flatpaks.sh` (for home folder).

### Instal·lació de programari Flatpak des d'una llista
Després d'importar el fitxer de configuració, en tornar a iniciar la sessió, **el programari Flatpak s'instal·larà en rerefons.**

_Si teniu cap dubte, utilitzeu el notificador d'incidències del GitHub._

{% include footer.html %}
