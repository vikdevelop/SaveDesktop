## Ukládání konfigurace

**Tato funkce je k dispozici od verze: `3.3`**

Pokud dáváte přednost rozhraní příkazového řádku (CLI) před grafickým uživatelským rozhraním (GUI), SaveDesktop kromě ukládání konfigurace v grafickém uživatelském rozhraní umožňuje ukládat konfiguraci i v CLI.

### Jak tedy postupovat?
**1. Otevřete terminál**

Můžete jej otevřít z nabídky aplikací nebo pomocí klávesové zkratky Ctrl+Alt+T.

**2. Zadejte příkaz**

Do terminálu zadejte následující příkaz:
- Pokud máte SaveDesktop nainstalovaný jako balíček Flatpak, použijte následující příkaz:

 ```
 flatpak run io.github.vikdevelop.SaveDesktop --save-now
 ```

- pokud máte SaveDesktop nainstalovaný jako Snap nebo nativní balíček, použijte: 
  ```
  saveesktop --save-now
  ```

Při použití této metody se používají parametry z grafického uživatelského rozhraní, konkrétně parametry z režimu pravidelného ukládání, jako je formát názvu souboru a vybraná složka pro pravidelné ukládání souborů. Pomocí této metody můžete konfiguraci uložit kdykoli chcete, bez ohledu na zvolený interval periodického ukládání.

## Import konfigurace

**Tato funkce je k dispozici od verze: `3.2.2`**

Kromě importu konfigurace v grafickém uživatelském rozhraní umožňuje SaveDesktop také importovat konfiguraci v rozhraní příkazového řádku (CLI), které můžete použít v případě, že se vaše desktopové prostředí rozbije.

### Jak tedy postupovat?
**1. Otevřete terminál**

Můžete jej otevřít z nabídky aplikací nebo pomocí klávesové zkratky Ctrl+Alt+T.

**2. Zadejte příkaz**

Do terminálu zadejte následující příkaz:
- Pokud máte SaveDesktop nainstalovaný jako balíček Flatpak, použijte následující příkaz:

 ```
 flatpak run io.github.vikdevelop.SaveDesktop --import-config /path/to/filename.sd.tar.gz
 ```

- pokud máte SaveDesktop nainstalovaný jako Snap nebo nativní balíček, použijte: 
  ```
  saveesktop --import-config /path/to/filename.sd.tar.gz
  ```

**Poznámka**:
- místo `/path/to/filename.sd.tar.gz` zadejte cestu ke konfiguračnímu archivu, který chcete importovat, například: `/home/user/Downloads/myconfig.sd.tar.gz`



{% include footer.html %}
