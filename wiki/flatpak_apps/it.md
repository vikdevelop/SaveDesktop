# Salvataggio, importazione e sincronizzazione delle app Flatpak

Save Desktop consente di salvare, importare e sincronizzare le applicazioni Flatpak insieme ai relativi dati utente, oltre a icone, temi, impostazioni ed estensioni.

## Dove posso trovarlo?

Le opzioni relative a Flatpak si trovano nella finestra di dialogo **Seleziona elementi di configurazione**.
Puoi aprirla dal menu dell'intestazione (tre puntini nella barra del titolo della finestra).

## Opzioni disponibili

### Elenco delle app Flatpak installate

Salva e ripristina l'elenco delle applicazioni Flatpak installate.

### Dati utente delle app Flatpak installate

Consente di includere i dati utente delle applicazioni Flatpak selezionate.
Clicca sul pulsante **">"** per scegliere le app di cui salvare i dati.

### Mantieni app e dati Flatpak installati (abilitato per impostazione predefinita)

Se abilitata, Save Desktop **NON rimuoverà le applicazioni Flatpak o i relativi dati che non sono presenti nell'archivio**.

Se disabilitata, Save Desktop **rimuoverà tutte le app Flatpak installate che non sono elencate nell'archivio importato, inclusi i relativi dati utente**.

⚠️ **Attenzione:**
Disattiva questa opzione solo se desideri che il tuo sistema corrisponda esattamente all'archivio importato. Le applicazioni rimosse e i relativi dati **non possono essere recuperati**.

## Come funziona l'importazione?

Dopo aver selezionato un archivio o una cartella, ti verrà chiesto quali elementi di configurazione importare.
Fai clic su **Applica** per avviare il processo di importazione.

Ordine di importazione:

1. Configurazione desktop (icone, temi, font, estensioni, impostazioni, ecc.)
2. Applicazioni Flatpak e relativi dati utente (dopo il successivo accesso)

L'installazione e la rimozione di Flatpak iniziano **dopo aver effettuato nuovamente l'accesso al sistema**.

### Modalità di sincronizzazione

In modalità di sincronizzazione, le applicazioni Flatpak vengono elaborate **immediatamente dopo il termine della sincronizzazione** (non è necessario alcun nuovo accesso).

## Nota importante

Se l'opzione **Mantieni app e dati Flatpak installati** è disattivata e hai installato applicazioni Flatpak non incluse nell'archivio importato, queste verranno **rimosse definitivamente insieme ai relativi dati utente**.

{% include footer.html %}