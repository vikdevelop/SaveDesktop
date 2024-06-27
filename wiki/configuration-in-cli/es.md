# Importar la configuración en la interfaz CLI
## Saving configuration

**This feature is available from version: `3.3`**

If you prefer command-line interface (CLI) before graphical user interface (GUI), SaveDesktop in addition to saving configuration in the GUI, allows you save configuration in the CLI.

### So how to proceed?

**1. Open a terminal**

You can open it from the applications menu, or by using the Ctrl+Alt+T keyboard shortcut.

**2. Type the command to import the configuration**

Enter the following command in the terminal:
- if you have SaveDesktop installed as a Flatpak package, use the following:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --save-now
     ```

- if you have SaveDesktop installed as a Snap or native package, use:
     ```
     savedesktop --save-now
     ```

When using this method, it uses parameters from the GUI, specifically parameters from the periodic saving mode, such as filename format and selected folder for periodic saving files. You can save the configuration with this method whenever you want, regardless of the selected periodic saving interval.

## Importing configuration

*Esta función está disponible a partir de la versión: `3.2.2`*

Además de importar la configuración en la GUI, SaveDesktop también le permite importar la configuración en la interfaz de línea de comandos (CLI), que puede utilizar en caso de que su entorno de escritorio se rompa.

### Entonces, ¿cómo proceder?

**1. Abrir un terminal**

Puede abrirlo desde el menú de aplicaciones, o usando el atajo de teclado Ctrl+Alt+T.

**2. Escriba el comando para importar la configuración**

Introduzca el siguiente comando en el terminal:
- si tiene SaveDesktop instalado como un paquete Flatpak, utilice lo siguiente:

     ```
     Ejecute flatpak io.github.vikdevelop.SaveDesktop --import-config /ruta/a/nombre de archivo.sd.tar.gz
     ```

- si tiene SaveDesktop instalado como un paquete Snap o nativo, utilice: 
     ```
     savedesktop --import-config /ruta/a/nombre de archivo.sd.tar.gz
     ```

**Nota**:
- en lugar de `/path/to/filename.sd.tar.gz`, introduzca la ruta al archivo de configuración que desea importar, por ejemplo: `/home/user/Downloads/myconfig.sd.tar.gz`

_Si tiene alguna duda, utilice el notificador de incidencias de GitHub._
