# Šifrování archivu
**Tato funkce je k dispozici od verze: 3.3**

Pokud chcete zašifrovat konfigurační archiv, ať už z důvodu ochrany dat nebo z jiných důvodů, můžete použít funkci šifrování archivu v aplikaci SaveDesktop. Jak tedy funguje a jak ji nastavit?

## Jak to funguje?
Pokud je tato funkce povolena, SaveDesktop vás vždy požádá o vytvoření hesla pro nový archiv konfigurace. Kritéria pro heslo zahrnují alespoň 12 znaků, jedno velké písmeno, jedno malé písmeno a jeden speciální znak. Pokud heslo tato kritéria nesplňuje, nebude možné v ukládání konfigurace pokračovat.

Archiv bude uložen jako archiv ZIP (protože Tar nepodporuje funkci ochrany heslem), a pokud jej budete chtít rozbalit, budete vyzváni k zadání hesla, které jste použili při ukládání konfigurace. Totéž platí v případě importu konfigurace.

Pokud jste heslo zapomněli, nebude možné archiv rozbalit a použít jej v procesu importu konfigurace.

> [!WARNING]  
> Soubory pro pravidelné ukládání (zatím) nelze chránit heslem. Šifrované archivy zatím není možné použít při synchronizaci.

## Jak to nastavit?
Ve verzi 3.3 bylo rozhraní mírně upraveno, konkrétně se nyní sekce pro pravidelné ukládání nachází pod tlačítkem "Další možnosti". Na stejném místě se nachází sekce šifrování archivu. Klikněte tedy na již zmíněné tlačítko a zapněte přepínač Šifrování archivu.



{% include footer.html %}
