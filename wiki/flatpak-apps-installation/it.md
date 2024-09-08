
# Salva le app Flatpak installate e installale dall'elenco
Dalla versione 2.5, SaveDesktop consente di salvare le applicazioni Flatpak installate e installarle da un elenco. Quindi, come funziona?

### Salvataggio delle applicazioni Flatpak installate
È possibile salvare un elenco delle applicazioni Flatpak installate dalla directory di sistema /var/lib/flatpak/app e dalla directory home ~/.local/share/flatpak/app. Nell'archivio di configurazione salvato, l'elenco delle applicazioni Flatpak installate è etichettato come installato_flatpaks.sh (per la directory di sistema) e installato_utente_flatpaks.sh (per la cartella home).

### Installazione delle applicazioni Flatpak dall'elenco
Dopo aver importato il file di configurazione salvato ed aver effettuato nuovamente l'accesso, **le applicazioni Flatpak inizieranno l'installazione in background.**



{% include footer.html %}
