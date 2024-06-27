# Guarde las aplicaciones instaladas de Flatpak e instálelas desde la lista
Desde la versión 2.5, SaveDesktop permite guardar las aplicaciones de Flatpak instaladas e instalarlas desde una lista. ¿Cómo funciona?

### Guardar las aplicaciones instaladas de Flatpak
Es posible guardar una lista de aplicaciones Flatpak instaladas desde el directorio de sistema `/var/lib/flatpak/app`, y el directorio de usuario `~/.local/share/flatpak/app`. En el archivo de configuración guardado, la lista de aplicaciones Flatpak instaladas se etiqueta como `installed_flatpaks.sh` (para el directorio del sistema) e `installed_user_flatpaks.sh` (para la carpeta home).

### Instalar las aplicaciones de Flatpak de la lista
Tras importar el archivo de configuración guardado y volver a conectarse, **las aplicaciones de Flatpak comenzarán a instalarse en segundo plano.**

_Si tiene alguna duda, utilice el notificador de incidencias de GitHub._
