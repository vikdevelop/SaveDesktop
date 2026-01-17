# Ukládání, import a synchronizace aplikací Flatpak

Save Desktop vám umožňuje ukládat, importovat a synchronizovat aplikace Flatpak spolu s jejich uživatelskými daty, ikonami, motivy, nastaveními a rozšířeními.

## Kde to najdu?

Možnosti související s Flatpakem se nacházejí v dialogovém okně **Vybrat položky konfigurace**.
Otevřít jej můžete z hlavního menu (tři tečky v záhlaví okna).

## Dostupné možnosti

### Seznam nainstalovaných aplikací Flatpak

Uloží a obnoví seznam nainstalovaných aplikací Flatpak.

### Uživatelská data nainstalovaných aplikací Flatpak

Umožňuje zahrnout uživatelská data vybraných aplikací Flatpak.
Kliknutím na tlačítko **„>“** vyberte, u kterých aplikací se mají data uložit.

### Zachovat nainstalované aplikace Flatpak a data (ve výchozím nastavení povoleno)

Pokud je tato možnost povolena, Save Desktop **NEODSTRANÍ aplikace Flatpak ani jejich data, která nejsou přítomna v archivu**.

Pokud je tato možnost zakázána, Save Desktop **odstraní všechny nainstalované aplikace Flatpak, které nejsou uvedeny v importovaném archivu, včetně jejich uživatelských dat**.

⚠️ **Upozornění:**
Tuto možnost zakážte pouze v případě, že chcete, aby váš systém přesně odpovídal importovanému archivu. Odstraněné aplikace a jejich data **nelze obnovit**.

## Jak funguje import?

Po výběru archivu nebo složky budete dotázáni, které konfigurační položky mají být importovány.
Kliknutím na **Použít** spustíte proces importu.

Pořadí importu:

1. Konfigurace plochy (ikony, motivy, písma, rozšíření, nastavení atd.)
2. Aplikace Flatpak a jejich uživatelská data (po dalším přihlášení)

Instalace a odinstalace Flatpak se spustí **po opětovném přihlášení do systému**.

### Režim synchronizace

V režimu synchronizace jsou aplikace Flatpak zpracovány **ihned po dokončení synchronizace** (není nutné se znovu přihlašovat).

## Důležitá poznámka

Pokud je možnost **Ponechat nainstalované aplikace Flatpak a data** deaktivována a máte nainstalované aplikace Flatpak, které nejsou zahrnuty v importovaném archivu, budou **trvale odstraněny spolu s uživatelskými daty**.

{% include footer.html %}