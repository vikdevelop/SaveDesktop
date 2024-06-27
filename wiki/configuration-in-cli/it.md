# Importazione della configurazione nell'interfaccia CLI

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

**Questa funzionalità è disponibile dalla versione: `3.2.2`**

Oltre a importare la configurazione nella GUI, SaveDesktop ti consente anche di importare la configurazione nell'interfaccia a riga di comando (CLI), che puoi utilizzare nel caso in cui il tuo ambiente desktop si guasti.

### Quindi, come procedere?
**1. Apri un terminale**

Puoi aprirlo dal menu delle applicazioni o utilizzando la scorciatoia da tastiera Ctrl+Alt+T.

**2. Digita il comando per importare la configurazione**

Immettere il seguente comando nel terminale:
- se hai SaveDesktop installato come pacchetto Flatpak, utilizza quanto segue:

   ```
   flatpak run io.github.vikdevelop.SaveDesktop --import-config /path/to/filename.sd.tar.gz
   ```

- se hai SaveDesktop installato come Snap o pacchetto nativo, utilizza:
   ```
   savedesktop --import-config /percorso/del/nomefile.sd.tar.gz
   ```
      
**Nota**:
- invece di `/path/to/filename.sd.tar.gz`, inserisci il percorso dell'archivio di configurazione che desideri importare, ad esempio: `/home/user/Downloads/myconfig.sd.tar.gz`

_Se hai domande, puoi usare GitHub issues._
