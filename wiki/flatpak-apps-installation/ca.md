# Desa el programari Flatpak per ser instal·lat des d'una llista
Des de la versió 2.5, el SaveDesktop us permet desar el programari Flatpak existent i instal·lar-ho des d'una llista. Com funciona això?

### Desat del programari Flatpak instal·lat
És possible crear una llista del programari Flatpak existent a la carpeta `/var/lib/flatpak/app` del sistema, però no a el que es trobi a `~/.local/share/flatpak/app`. Al fitxer de configuració desat, la llista del programari Flatpak està etiquetat com a `installed_flatpaks.sh`.

### Instal·lació de programari Flatpak des d'una llista
Després d'importar el fitxer de configuració, en tornar a iniciar la sessió, **el programari Flatpak s'instal·larà en rerefons.**



{% include footer.html %}
