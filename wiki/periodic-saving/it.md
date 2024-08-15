# Salvataggio periodico
Oltre ai salvataggi manuali, SaveDesktop consente anche di salvare periodicamente la configurazione del desktop. Puoi scegliere tra le seguenti opzioni:
- **Quotidiano**:
   - Dopo aver effettuato l'accesso al sistema, SaveDesktop si avvia in background ed esegue il backup della configurazione. Se poi accedi nuovamente, non lo farà più, perché è già stato creato per quel giorno.
- **Settimanalmente**:
   - SaveDesktop esegue un backup della configurazione ogni lunedì se è selezionato "Settimanale". Se quel giorno il computer non è in funzione, SaveDesktop non lo farà il giorno successivo.
- **Mensile**:
   - Se è selezionato "Mensile", SaveDesktop esegue il backup il primo giorno del mese, ad es. 1 maggio, 1 giugno, 1 dicembre, ecc. Come per "Settimanale", se il computer non è in esecuzione quel giorno, SaveDesktop non lo eseguirà il giorno successivo.
- **Mai**:
   - Non succede nulla

### Dove sono archiviati i file di salvataggio periodici?
La directory predefinita per il salvataggio periodico è "/home/user/Downloads/SaveDesktop/archives", ma puoi scegliere una directory personalizzata.

### Formato del nome file
Se vuoi dare un formato di nome file per il salvataggio periodico dei file diverso da "Ultimaconfigurazione", è possibile, anche con gli spazi. Dalla versione 2.9.6, la variabile `{}` non funziona per impostare la data odierna perché ora, ad ogni salvataggio periodico, il file di backup originale viene sovrascritto.



{% include footer.html %}
