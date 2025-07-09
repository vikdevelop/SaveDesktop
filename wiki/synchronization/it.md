# Sincronizzazione tra computer in rete

Oltre a salvare la configurazione e importarla, Save Desktop consente anche di sincronizzarla tra i computer della rete utilizzando una cartella cloud condivisa o una cartella Syncthing condivisa.

## Configurazione sul primo computer
1. Apri la pagina **Sync** nell'app Save Desktop.
2. Fai clic su **"Configura il file di sincronizzazione".**
3. Apparirà una procedura guidata di configurazione rapida:
* Se utilizzi GNOME, Cinnamon, Budgie o una versione precedente di COSMIC, viene utilizzato il metodo **Account GNOME Online**.
* Per KDE Plasma o altri desktop, passa a **Rclone** (dovrai solo copiare un comando e incollarlo nel terminale).
* In alternativa, puoi utilizzare **Syncthing** facendo clic su **"Usa la cartella di Syncthing"** e selezionando una cartella sincronizzata.
4. Al termine della procedura guidata, si aprirà la finestra di dialogo **"Configura il file di sincronizzazione":
* Un **file di salvataggio periodico** (l'archivio di configurazione del desktop) inizierà a essere generato all'interno della cartella selezionata.
* Puoi facoltativamente modificare l'intervallo o il nome del file utilizzando il pulsante **"Modifica"**. 
5. Fai clic su **"Applica"**:
* Un secondo file, `SaveDesktop.json`, viene creato nella stessa cartella. Contiene il nome del file di sincronizzazione e l'intervallo di salvataggio.
* Ti verrà richiesto di **disconnetterti** dalla sessione affinché la sincronizzazione possa essere completamente attivata.

## Connessione su un altro computer
1. Sull'altro computer, accedi nuovamente alla pagina **Sincronizzazione**.
2. Fai clic su **"Connetti all'archivio cloud".**
3. Apparirà la stessa procedura guidata: scegli la cartella sincronizzata tramite GNOME OA, Rclone o Syncthing.
4. Dopo la procedura guidata:
* Si apre la finestra di dialogo **"Connetti all'archivio cloud".**
* Seleziona l'**intervallo di sincronizzazione** e abilita o disabilita la **Sincronizzazione bidirezionale**.
5. Fai clic su **"Applica":
* Ti verrà richiesto di **disconnetterti** o (se utilizzi la sincronizzazione manuale) verrai informato che puoi sincronizzare dal menu principale dell'app.
* Dopo aver effettuato nuovamente l'accesso, Save Desktop si connette alla cartella condivisa e sincronizza automaticamente la configurazione, con una notifica all'inizio e alla fine.

### Sincronizzazione bidirezionale
Se la **Sincronizzazione bidirezionale** è abilitata su entrambi i computer:
* Save Desktop copia le impostazioni di sincronizzazione (come intervallo e nome file) da una macchina all'altra,
* Questo mantiene i sistemi sincronizzati senza dover configurare manualmente ciascuno di essi.

## File utilizzati nella sincronizzazione
* **File di salvataggio periodico** – un archivio `.sd.zip` della configurazione del desktop, aggiornato regolarmente.
* **SaveDesktop.json** – un piccolo file di supporto che memorizza il nome del file e l'intervallo di salvataggio dell'archivio, utilizzato durante la configurazione della sincronizzazione.

{% include footer.html %}