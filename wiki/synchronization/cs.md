# Synchronizace mezi počítači v síti
## Jak ji nastavit?
### Co potřebujete?

**Na počítači 1:**
- ručně přiřazené IP adresy zařízení, které chcete synchronizovat, aby se IP adresa neměnila při každém zapnutí počítače. Je možné to nastavit prostřednictvím:

  **Nastavení routeru:**
  - [pro routery Asus](https://www.asus.com/support/FAQ/1000906/)
  - [pro routery Tp-link](https://www.tp-link.com/us/support/faq/170/)
  - [pro routery Tenda](https://www.tendacn.com/faq/3264.html)
  - [pro routery Netgear](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - pokud výše uvedené routery nemáte, otevřete nastavení routeru (URL: [192.168.1.1](http://192.168.1.1) nebo příbuzné) a v části DHCP serveru vyhledejte něco ve tvaru "Manually assign an IP to the DHCP list" nebo "Static IP" apod.
  
  **Balíčku `system-config-printer`:** <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
  - pokud nechcete nastavovat IP adresu ručně z rozhraní routeru, máte tiskárnu a nainstalovaný balíček `system-config-printer`, zkontrolujte zda jste zaškrtli položku "Sdílené" kliknutím na kartu "Tiskárna" v záhlaví. Pokud ne, zaškrtněte ji a restartujte systém. [Zde](https://github-production-user-asset-6210df.s3.amazonaws.com/83600218/272054218-ff17c19b-98f5-41fe-8f34-40de275f0da4.png) je snímek obrazovky, jak to má vypadat.

**Na počítači 2:**
- Zkontrolujte, zda jste připojeni ke stejné síti jako počítač 1.

### Nastavení synchronizace v aplikaci SaveDesktop
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

Na počítači 1 a 2 otevřete aplikaci SaveDesktop a přepněte na stránku Synchronizovat. Na počítači 1 klikněte na tlačítko "Nastavit synchronizační soubor", vyberte synchronizační soubor (váš soubor pravidelného ukládání) a zvolte interval pravidelné synchronizace. Poté zkopírujte adresu URL pro synchronizaci a na počítači 2 klikněte na tlačítko "Připojit se k jinému počítači" a zadejte zkopírovanou adresu URL pro synchronizaci z počítače 1.

Pokud chcete synchronizovat konfiguraci desktopového prostředí z počítače 2 do počítače 1, postupujte stejně.

**Aby se změny projevily, je nutné se odhlásit ze systému**.

## Pravidelná synchronizace
Můžete si vybrat mezi následujícími položkami:
- Denně
- Týdně (synchronizace probíhá každé úterý)
- Měsíčně (synchronizace probíhá každý druhý den v měsíci)
- Ručně (je možné synchronizovat konfiguraci z menu v záhlaví kliknutím na tři tečky)
- Nikdy (nic se neděje)



{% include footer.html %}
