# Pravidelné ukládání
Kromě ručního ukládání umožňuje SaveDesktop také pravidelné ukládání konfigurace desktopového prostředí. Můžete si vybrat z následujících možností:
- **Denně**: 
  - Po přihlášení do systému se SaveDesktop spustí na pozadí a zálohuje konfiguraci. Pokud se pak v tento den znovu přihlásíte, nebude to dělat znovu, protože pro tento den již byla vytvořena.
- **Týdně**:
  - Pokud je vybrána možnost "Týdně", SaveDesktop provede zálohu konfigurace každé pondělí. Pokud počítač v tento den není spuštěn, SaveDesktop ji následující den neprovede.
- **Měsíčně**:
  - Pokud je vybrána možnost "Měsíčně", SaveDesktop provede zálohu první den v měsíci, např. 1. května, 1. června, 1. prosince atd. Stejně jako u možnosti "Týdně", pokud počítač v tento den není spuštěn, SaveDesktop ji následující den neprovede.
- **Nikdy**:
  - Nic se neděje

### Kam se ukládají soubory pravidelného ukládání?
Výchozí adresář pro pravidelné ukládání je `/home/user/Downloads/SaveDesktop/archives`, ale můžete si zvolit vlastní adresář.

### Formát názvu souboru
Chcete-li zadat jiný formát názvu souboru pro pravidelné ukládání než `Latestconfiguration`, je to možné, a to i s mezerami. Od verze 2.9.6, nefunguje proměnná `{}`pro nastavení dnešního data, proto že je nyní při každém pravidelném ukládání přepsán původní soubor zálohy.



{% include footer.html %}
