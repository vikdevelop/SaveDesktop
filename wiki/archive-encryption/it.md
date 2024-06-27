# Cifratura dell'archivio
**Questa funzionalità è disponibile dalla versione: 3.3**

Se desideri crittografare l'archivio di configurazione, sia per motivi di protezione dei dati che per altro, puoi utilizzare la funzione di crittografia dell'archivio nell'app SaveDesktop. Quindi, come funziona e come configurarlo?

## Come funziona?
Se questa funzione è abilitata, SaveDesktop ti chiederà sempre di creare una password per il tuo nuovo archivio della configurazione. I criteri per la password includono almeno 8 caratteri, una lettera maiuscola, una lettera minuscola e un carattere speciale. Se la password non soddisfa questi criteri non sarà possibile continuare a salvare la configurazione.

The archive will be saved as a ZIP archive (because Tar doesn't support the password protection feature), and if you want to extract it, you will be asked to enter the password that you used in the saving configuration process. The same applies in the case of configuration import.

If you forgot the password, it will not possible to extract the archive and use it in the importing configuration process.

> [!WARNING]    
> I file di salvataggio periodico non sono (finora) disponibili per essere protetti con una password. Ad oggi, non è possibile sincronizzare gli archivi crittografati.

## Come configurarlo?
Nella versione 3.3 l'interfaccia è stata leggermente modificata, nello specifico la sezione di salvataggio periodico si trova ora sotto il pulsante "Ulteriori opzioni". Nello stesso posto si trova la sezione di crittografia dell'archivio. Quindi fai clic sul pulsante già menzionato e abilita l'interruttore di crittografia dell'archivio.

_Se hai domande, puoi usare GitHub issues._
