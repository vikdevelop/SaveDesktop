# Synchronizace mezi počítači v síti

Kromě uložení konfigurace a jejího importu umožňuje SaveDesktop také její synchronizaci mezi počítači v síti pomocí sdílené cloudové složky nebo sdílené složky Syncthing.

## Nastavení prvního počítače
1. V aplikaci SaveDesktop otevřete stránku **Sync**.
2. Klepněte na tlačítko **„Nastavit synchronizační soubor “**.
3. Zobrazí se průvodce rychlým nastavením:
   * Pokud používáte prostředí GNOME, Cinnamon, Budgie nebo starší COSMIC, použije se metoda **GNOME Online Accounts**.
   * V případě prostředí KDE Plasma nebo jiných desktopů se přepne na **Rclone** (stačí zkopírovat příkaz a vložit jej do terminálu).
   * Alternativně můžete použít **Syncthing** kliknutím na **„Použít místo toho složku Syncthing “** a výběrem synchronizované složky.
4. Po dokončení průvodce se otevře dialogové okno **„Nastavit synchronizační soubor “**:
   * Ve vybrané složce se začne generovat **soubor pro periodické ukládání** (váš archív konfigurace pracovní plochy).
   * Interval nebo název souboru můžete volitelně změnit pomocí tlačítka **„Změnit “**.
5. Klepněte na tlačítko **„Použít “**:
   * Ve stejné složce se vytvoří druhý soubor, `SaveDesktop.json`. Obsahuje název synchronizačního souboru a interval ukládání.
   * Budete vyzváni k **odhlášení** z relace, aby se synchronizace mohla plně aktivovat.

## Připojení k jinému počítači
1. Na druhém počítači znovu přejděte na stránku **Synchronizace**.
2. Klepněte na tlačítko **„Připojit ke cloudovému úložišti “**.
3. Zobrazí se stejný průvodce - vyberte složku synchronizovanou prostřednictvím GNOME OA, Rclone nebo Syncthing.
4. Po zobrazení průvodce:
   * Otevře se dialogové okno **„Připojit ke cloudovému úložišti “**.
   * Vyberte **interval synchronizace** a povolte nebo zakažte **obousměrnou synchronizaci**.
5. Klikněte na tlačítko **„Použít “**:
   * Budete vyzváni k **odhlášení** nebo (pokud používáte ruční synchronizaci) informováni, že můžete synchronizovat z nabídky v záhlaví aplikace.
   * Po opětovném přihlášení se aplikace SaveDesktop připojí ke sdílené složce a automaticky synchronizuje vaši konfiguraci s upozorněním na začátku a na konci.

### Obousměrná synchronizace
Pokud je **obousměrná synchronizace** povolena na obou počítačích:
* SaveDesktop kopíruje nastavení synchronizace (například interval a název souboru) z jednoho počítače na druhý,
* Díky tomu jsou vaše systémy synchronizovány, aniž byste museli každý z nich nastavovat ručně.

## Soubory použité při synchronizaci
* **Periodický ukládací soubor** - archiv `.sd.zip` konfigurace pracovní plochy, který je pravidelně aktualizován.
* **SaveDesktop.json** - malý pomocný soubor, který ukládá název archivu a interval ukládání, používaný při nastavení synchronizace.
