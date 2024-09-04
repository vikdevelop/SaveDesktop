# Sincronizzazione tra computer in rete
#### Requisiti
- È necessario che sia stata creata una cartella da sincronizzare con l'archivio cloud su ciascun computer che si desidera sincronizzare. Questo può essere fatto utilizzando:

  <details>
    <summary>
    <b>Account online GNOME</b>
    <p>(per gli ambienti desktop GNOME, Cinnamon, COSMIC (vecchio) e Budgie)</p>
    </summary>

    - Apri le Impostazioni GNOME
    - Vai alla sezione Account online e seleziona il tuo servizio di cloud storage

    ![OnlineAccounts.png](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/webpage/wiki/synchronization/screenshots/OnlineAccounts_en.png)

  </details>


  <details>
    <summary>
    <b>Rclone</b>
    <p>(per altri ambienti desktop)</p>
    </summary>

    - Installa Rclone
    ```
    sudo -v ; curl https://rclone.org/install.sh | sudo bash
    ```

    - Imposta Rclone usando questo comando, che crea la cartella cloud drive, imposta Rclone e monta la cartella
    ```
    mkdir -p ~/drive &amp;&amp; rclone config create drive your-cloud-drive-service &amp;&amp; nohup rclone mount drive: ~/drive --vfs-cache-mode writes &amp; echo "L'unità è stata montata correttamente"
    ```
    * Invece di `your-cloud-drive-service` usa il nome del tuo servizio cloud drive, come `drive` (per Google Drive), `onedrive`, `dropbox`, ecc.

    - Consenti l'accesso alla cartella creata nell'[app Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal).
    </details>

  
## Impostazione della sincronizzazione nell'app SaveDesktop
Sul primo computer:
1. Apri l'app SaveDesktop
2. Nella pagina Sincronizzazione, fai clic sul pulsante "Imposta file di sincronizzazione" e poi sul pulsante "Modifica"
3. Fai clic su "Salvataggio periodico" e seleziona la cartella sincronizzata con il tuo archivio cloud come cartella di salvataggio periodico
4. Se il file di salvataggio periodico non esiste, fai clic sul pulsante Crea

Sul secondo computer:
1. Apri l'app SaveDesktop
2. Vai alla pagina Sincronizzazione e clicca sul pulsante "Connetti allo storage cloud".
3. Clicca sul pulsante "Seleziona cartella unità cloud" e seleziona la cartella sincronizzata con lo stesso storage cloud del primo computer.
4. Seleziona l'intervallo di sincronizzazione periodica, perché se lo lasci su Mai, la sincronizzazione non funziona.

Per impostare la sincronizzazione bidirezionale, assicurati di aver selezionato la stessa cartella cloud nella finestra di dialogo "Connetti allo storage cloud" sul primo computer, di aver selezionato l'intervallo di sincronizzazione periodica e di aver abilitato l'opzione "Sincronizzazione bidirezionale".

### Sincronizzazione periodica
Puoi scegliere tra le seguenti opzioni:
- Giornaliera
- Settimanale (la sincronizzazione avviene ogni martedì)
- Mensile (la sincronizzazione avviene ogni secondo giorno del mese)
- Manuale (è possibile sincronizzare la configurazione dal menu nella barra dell'intestazione cliccando sui tre puntini)
- Mai (non succede nulla)

{% include footer.html %}
