# Sincronizzazione tra computer in rete
## Come configurarlo?
### Di cosa hai bisogno?
**Sul computer 1:**
- assegna manualmente gli indirizzi IP dei tuoi dispositivi che desideri sincronizzare in modo che l'indirizzo IP non cambi ogni volta che accendi il computer. E' possibile impostarlo tramite:

   **Impostazioni del router:**
   - [per router Asus](https://www.asus.com/support/FAQ/1000906/)
   - [per router Tp-link](https://www.tp-link.com/us/support/faq/170/)
   - [per router Tenda](https://www.tendacn.com/faq/3264.html)
   - [per router Netgear](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
   - se non disponi dei router sopra indicati, apri le impostazioni del router (URL: [192.168.1.1](http://192.168.1.1) o correlato) e cerca nella sezione del server DHCP qualcosa sotto forma di "Assegna manualmente un IP nell'elenco DHCP" o "IP statico", ecc.
   
   **`system-config-printer` package:** <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
   - se non vuoi impostare manualmente l'indirizzo IP dall'interfaccia del router e se hai una stampante e hai installato il pacchetto `system-config-printer`, controlla di aver selezionato l'opzione "Condivisa" facendo clic sulla scheda Stampante nella barra dell'intestazione. In caso contrario, spuntala e riavvia il sistema. [Qui](https://github-production-user-asset-6210df.s3.amazonaws.com/83600218/272054218-ff17c19b-98f5-41fe-8f34-40de275f0da4.png) è uno screenshot di come dovrebbe essere.

**Sul computer 2:**
- Controlla se sei connesso alla stessa rete del computer 1.

### Impostare la sincronizzazione nell'app SaveDesktop
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

Sui computer 1 e 2, apri l'applicazione SaveDesktop e passa alla pagina di sincronizzazione. Sul computer 1, fai clic sul pulsante "Imposta il file di sincronizzazione", seleziona il file di sincronizzazione (il tuo file di salvataggio periodico) e seleziona un intervallo di sincronizzazione periodica. Quindi copia l'URL per la sincronizzazione e, sul computer 2, fai clic sul pulsante "Connetti con un altro computer" e inserisci l'URL copiato per la sincronizzazione dal computer 1.
Se desideri sincronizzare la configurazione DE dal computer 2 al computer 1, segui la stessa procedura.

**Affinché le modifiche abbiano effetto è necessario disconnettersi dal sistema**

## Sincronizzazione periodica
Puoi scegliere tra i seguenti articoli:
- Quotidiano
- Settimanale (la sincronizzazione avviene ogni martedì)
- Mensile (la sincronizzazione avviene ogni secondo giorno del mese)
- Manualmente (è possibile sincronizzare la configurazione dal menu nella barra dell'intestazione cliccando sui tre punti)
- Never (nothing's happening)

_Se hai domande, puoi usare GitHub issues._

{% include footer.html %}
