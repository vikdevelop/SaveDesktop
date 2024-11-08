
## Desant la configuració

**Aquesta característica és disponible des de la versió: `3.3`**

Tant si preferiu la línia d'ordres (CLI) com ara un entorn gràfic (GUI), el SaveDesktop us permet dur a terme la tasca de totes dues formes.

### Com procedir?
**1. Obriu la terminal**

Es pot fer des del menú d'aplicacions, o mitjançant la drecera de teclat Ctrl+Alt+T.

**2. Inseriu l'ordre per a importar la configuració**

Inseriu l'ordre següent a la consola d'ordres:
- Si heu instal·lat el SaveDesktop com a paquet Flatpak, utilitzeu aquesta ordre:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --save-now
     ```

- Si heu instal·lat el SaveDesktop com a paquet Snap o paquet natiu, llavors empreu:  
     ```
     savedesktop --save-now
     ```

En utilitzar aquest mètode, s'empraran els paràmetres de la interfície gràfica (GUI). Específicament els paràmetres del desament periòdic, com ara el format de nom de fitxer i la carpeta de destinació on desar els fitxers. Podeu desar la configuració amb aquest mètode sempre que vulgueu, independentment de l'interval de desament automàtic triat.

## Important la configuració

**Aquesta característica és disponible des de la versió: `3.2.2`**

A més de la importació mitjançant la interfície gràfica (GUI), el SaveDesktop també us permet importar la configuració mitjançant la línia d'ordres (CLI), que podeu utilitzar en cas que el vostre entorn d'escriptori es trenqui.

### Com procedir?
**1. Obriu la terminal**

Es pot fer des del menú d'aplicacions, o mitjançant la drecera de teclat Ctrl+Alt+T.

**2. Inseriu l'ordre per a importar la configuració**

Inseriu l'ordre següent a la consola d'ordres:
- Si heu instal·lat el SaveDesktop com a paquet Flatpak, utilitzeu aquesta ordre:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --import-config /ruta/del/fitxer.sd.tar.gz
     ```

- Si heu instal·lat el SaveDesktop com a paquet Snap o paquet natiu, llavors empreu:  
     ```
     savedesktop --import-config /ruta/del/fitxer.sd.tar.gz
     ```

**Nota**:
- En comptes de `/ruta/del/fitxer.sd.tar.gz`, indiqueu la ruta real on es troba el fitxer de configuració que voleu importar, com ara: `/home/benet/Documents/config.sd.tar.gz`



{% include footer.html %}
