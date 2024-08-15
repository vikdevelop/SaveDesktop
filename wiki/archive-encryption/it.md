# Cifratura dell'archivio
**Questa funzionalità è disponibile dalla versione: 3.3**

Se desideri crittografare l'archivio di configurazione, sia per motivi di protezione dei dati che per altro, puoi utilizzare la funzione di crittografia dell'archivio nell'app SaveDesktop. Quindi, come funziona e come configurarlo?

## Come funziona?
Se questa funzione è abilitata, SaveDesktop ti chiederà sempre di creare una password per il tuo nuovo archivio della configurazione. I criteri per la password includono almeno 12 caratteri, una lettera maiuscola, una lettera minuscola e un carattere speciale. Se la password non soddisfa questi criteri non sarà possibile continuare a salvare la configurazione.

L'archivio verrà salvato come archivio ZIP (perché Tar non supporta la funzione di protezione tramite password) e, se desideri estrarlo, ti verrà chiesto di inserire la password che hai utilizzato nel processo di configurazione del salvataggio. Lo stesso vale in caso di importazione della configurazione.

Se si dimentica la password non sarà possibile estrarre l'archivio ed utilizzarlo nel processo di importazione della configurazione.

> [!WARNING]    
> I file di salvataggio periodico non sono (finora) disponibili per essere protetti con una password. Ad oggi, non è possibile sincronizzare gli archivi crittografati.

## Come configurarlo?
Nella versione 3.3 l'interfaccia è stata leggermente modificata, nello specifico la sezione di salvataggio periodico si trova ora sotto il pulsante "Ulteriori opzioni". Nello stesso posto si trova la sezione di crittografia dell'archivio. Quindi fai clic sul pulsante già menzionato e abilita l'interruttore di crittografia dell'archivio.



{% include footer.html %}
