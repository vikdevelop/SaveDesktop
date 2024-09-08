{% include head.html %}

# Uložit nainstalované aplikace Flatpak a nainstalovat je ze seznamu
Od verze 2.5 umožňuje SaveDesktop ukládat nainstalované aplikace Flatpak a instalovat je ze seznamu. Jak to tedy funguje?

### Ukládání nainstalovaných aplikací Flatpak
Seznam nainstalovaných aplikací Flatpak je možné uložit ze systémového adresáře /var/lib/flatpak/app a domovského adresáře ~/.local/share/flatpak/app. Seznam nainstalovaných aplikací Flatpak je v konfiguračním archivu označen jako installed_flatpaks.sh pro systémový adresář a installed_user_flatpaks.sh pro domovský adresář.

### Instalace aplikací Flatpak ze seznamu
Po importu uloženého konfiguračního souboru a opětovném přihlášení se **na pozadí začnou instalovat aplikace Flatpak.**



{% include footer.html %}
