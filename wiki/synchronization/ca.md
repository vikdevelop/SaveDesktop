# Sincronització entre ordinadors de la xarxa
## Com es configura?
###  Quins són els requisits?
**A l'ordinador 1:**
- Assigneu una IP manual als equips que voleu sincronitzar perquè aquesta no canviï cada vegada que els inicieu. Això és possible mitjançant:

  **Configuració de l'encaminador:**
  - [Asus](https://www.asus.com/support/FAQ/1000906/)
  - [Netgear](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - [Tenda](https://www.tendacn.com/faq/3264.html)
  - [Tp-link](https://www.tp-link.com/us/support/faq/170/)
  - Si no teniu cap d'aquests fabricants, proveu accedint des d'un navegador com ara el Firefox a l'adreça del vostre dispositiu (URL: [192.168.1.1](http://192.168.1.1) o similars) i cerqueu dins la secció *DHCP* quelcom semblant a «IP estàtica», «exclusió DHCP», etc. O bé contacteu amb el fabricant de l'aparell o el proveïdor de la vostra connexió a Internet.

  **`system-config-printer` package:**  <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
  - Si no voleu assignar una IP manual a l'encaminador i teniu una impressora instal·lada al vostre sistema, a més del paquet `system-config-printer`, verifiqueu que l'opció «Compartida» està activada al panell principal de la impressora. En cas contrari, activeu aquesta opció i reinicieu el sistema. [Aquí](https://raw.githubusercontent.com/BennyBeat/SaveDesktop/1602010b7ef88f3fb0eb1010af33571f0c548eb3/translations/wiki/ca-Printer.png) teniu una captura de pantalla amb la configuració idònia.

**A l'ordinador 2:**
- Verifiqueu que està connectat a la mateixa xarxa que l'ordinador 1.

### Configuració de la sincronització a l'aplicació SaveDesktop
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

On computer 1 and 2, open the SaveDesktop application and switch to the Sync page. On computer 1, click on the button "Set up the sync file", select the synchronization file (your periodic saving file), and select a periodic synchronization interval. Then copy the URL for synchronization, and on computer 2, click on the button "Connect with other computer" and enter the copied URL for synchronization from computer 1.

Si voleu sincronitzar l'entorn d'escriptori de l'ordinador 2 a l'1, les passes són les mateixes.

**És necessari tancar i tornar a obrir la sessió per aplicar els canvis**

## Sincronització periòdica
Podeu triar entre els elements següents:
- Diàriament
- Setmanalment (la sincronització es duu a terme cada dimarts)
- Mensualment (la sincronització es duu a terme el segon dia de cada mes)
- Manualment (és possible realitzar la sincronització en qualsevol moment des del menú principal en fer clic als tres punts)
- Mai (no es duu a terme cap canvi)

_Si teniu cap dubte, utilitzeu el notificador d'incidències del GitHub._

{% include footer.html %}
