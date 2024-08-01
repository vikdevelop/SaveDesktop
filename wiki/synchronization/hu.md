# Azonos hálózaton lévő számítógépek szinkronizálása
## Hogyan állítsd be?
### Mire lesz szükséged?
**On computer 1:**
- a szinkronizálni kívánt eszközökhöz manuálisan hozzárendelt IP címek, amely biztosítja, hogy az IP cím nem változik meg minden alkalommal, amikor a számítógépet bekapcsolod. It is possible to set it via:

  **Router settings:**
  - [Asus router esetén](https://www.asus.com/support/FAQ/1000906/)
  - [Tp-link router esetén](https://www.tp-link.com/us/support/faq/170/)
  - [Tenda router esetén](https://www.tendacn.com/faq/3264.html)
  - [Netgear router esetén](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - más márkák esetén, nyisd meg a router admin oldalát (URL: [192.168.1.1](http://192.168.1.1) or related) és a DHCP szerver résznél keress az alábbiakhoz hasonló beállításokat, mint "IP manuális hozzárendelése DHCP listához" vagy "Statikus IP", stb.
  
  **`system-config-printer` package:** <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
  - if you don't want to set the IP address manually from the router interface, and if you have a printer and installed `system-config-printer` package, check if you ticked the option "Shared" by clicking Printer tab on the header bar. If not, please tick it and reboot the system. [Here](https://github-production-user-asset-6210df.s3.amazonaws.com/83600218/272054218-ff17c19b-98f5-41fe-8f34-40de275f0da4.png) is a screenshot, what it's supposed to look like

**On computer 2:**
- Check if you are connected to the same network as computer 1.

### Állítsa be a szinkronizálást a SaveDesktop alkalmazásban
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

On computer 1 and 2, open the SaveDesktop application and switch to the Sync page. On computer 1, click on the button "Set up the sync file", select the synchronization file (your periodic saving file), and select a periodic synchronization interval. Then copy the URL for synchronization, and on computer 2, click on the button "Connect with other computer" and enter the copied URL for synchronization from computer 1.

Ha szinkronizálni szeretnéd az asztali környezet konfigurációját a 2-es számítógépről az 1-es számítógépre, kövesd ugyanezt az eljárást.

**A módosítások életbe lépéséhez ki kell jelentkezni a rendszerből**

## Időszakos szinkronizálás
Az alábbi tételek közül választhatsz:
- Naponta
- Hetente (a szinkronizálás minden kedden történik)
- Havonta (a szinkronizálás a hónap minden második napján történik)
- Never (nothing's happening)

_Ha bármi kérdésed lenne, használd a Github Issues-t._

{% include footer.html %}
