# Ukládání a import konfigurace v rozhraní CLI
## Saving configuration

**This feature is available from version: `3.3`**

If you prefer command-line interface (CLI) before graphical user interface (GUI), SaveDesktop in addition to saving configuration in the GUI, allows you save configuration in the CLI.

## Jak tedy postupovat?
**1. Otevřete terminál**

Můžete jej otevřít z nabídky aplikací nebo pomocí klávesové zkratky Ctrl+Alt+T.

**2. Zadejte příkaz pro import konfigurace**

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

**2. Zadejte příkaz pro import konfigurace**

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

_Máte-li jakékoliv otázky, můžete použít Github issues._
