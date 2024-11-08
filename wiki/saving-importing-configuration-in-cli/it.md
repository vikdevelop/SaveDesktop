
## Salvataggio della configurazione

**Questa funzionalità è disponibile dalla versione: `3.3`**

Se preferisci l'interfaccia della riga di comando (CLI) all'interfaccia utente grafica (GUI), SaveDesktop oltre a salvare la configurazione nella GUI, ti consente di salvare la configurazione nella CLI.

### Quindi, come procedere?
**1. Apri un terminale**

Puoi aprirlo dal menu delle applicazioni o usando la scorciatoia da tastiera Ctrl+Alt+T.

**2. Inserisci il comando**

Inserisci il seguente comando nel terminale:
- se hai installato SaveDesktop come pacchetto Flatpak, usa quanto segue:
     ```
     flatpak run io.github.vikdevelop.SaveDesktop --save-now
     ```
- se hai installato SaveDesktop come pacchetto Snap o nativo, usa:
     ```
     savedesktop --save-now
     ```

Quando si utilizza questo metodo, vengono utilizzati i parametri della GUI, in particolare i parametri della modalità di salvataggio periodico, come il formato del nome file e la cartella selezionata per il salvataggio periodico dei file. Puoi salvare la configurazione con questo metodo ogni volta che vuoi, indipendentemente dall'intervallo di salvataggio periodico selezionato.

## Importazione della configurazione

**Questa funzionalità è disponibile dalla versione: `3.2.2`**

Oltre a importare la configurazione nella GUI, SaveDesktop ti consente anche di importare la configurazione nell'interfaccia a riga di comando (CLI), che puoi utilizzare nel caso in cui il tuo ambiente desktop si guasti.

### Quindi, come procedere?
**1. Apri un terminale**

Puoi aprirlo dal menu delle applicazioni o usando la scorciatoia da tastiera Ctrl+Alt+T.

**2. Inserisci il comando**

Inserisci il seguente comando nel terminale:
- se hai installato SaveDesktop come pacchetto Flatpak, usa quanto segue:
     ```
     flatpak run io.github.vikdevelop.SaveDesktop --import-config /path/to/filename.sd.tar.gz
     ```
- se hai installato SaveDesktop come pacchetto Snap o nativo, usa:
     ```
     savedesktop --import-config /path/to/filename.sd.tar.gz
     ```
      
**Nota**:
- invece di `/path/to/filename.sd.tar.gz`, inserisci il percorso dell'archivio di configurazione che desideri importare, ad esempio: `/home/user/Downloads/myconfig.sd.tar.gz`



{% include footer.html %}
