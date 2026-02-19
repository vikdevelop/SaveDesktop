# Spremanje, uvoz i sinkroniziranje Flatpak aplikacija

Save Desktop omogućuje spremanje, uvoz i sinkroniziranje Flatpak aplikacija zajedno s njihovim korisničkim podacima, kao i ikona, tema, postavki i proširenja.

## Gdje mogu to pronaći?

Opcije vezane uz Flatpak nalaze se u dijaloškom okviru **Odaberi stavke konfiguracije**.
Može se otvoriti iz izbornika zaglavlja (tri točkice u naslovnoj traci prozora).

## Dostupne opcije

### Popis instaliranih Flatpak aplikacija

Sprema i obnavlja popis instaliranih Flatpak aplikacija.

### Korisnički podaci instaliranih Flatpak aplikacija

Omogućuje uključivanje korisničkih podataka odabranih Flatpak aplikacija.
Klikni gumb **">"** za biranje aplikacija za koje se trebaju spremiti podaci.

### Zadrži instalirane Flatpak aplikacije i podatke (standardno aktivirano)

Kada je aktivirano, Save Desktop **neće uklanjati Flatpak aplikacije ili njihove podatke koji nisu prisutni u arhivi**.

Kada je deaktivirano, Save Desktop će **ukloniti sve instalirane Flatpak aplikacije koje nisu navedene u uvezenoj arhivi – uključujući njihove korisničke podatke**.

⚠️ **Upozorenje:**
Deaktiviraj ovu opciju samo ako namjerno želiš da tvoj sustav točno odgovara uvezenoj arhivi. Uklonjene aplikacije i njihovi podaci **se ne mogu obnoviti**.

## Kako funkcionira uvoz?

Nakon odabira arhive ili mape će se pojaviti pitanje, koje stavke konfiguracije želiš uvesti.
Klikni **Primijeni** za pokretanje uvoza.

Redoslijed uvoza:

1. Konfiguracija radne površine (ikone, teme, fontovi, proširenja, postavke i sl.)
2. Flatpak aplikacije i njihovi korisnički podaci (nakon sljedeće prijave)

Instalacija i uklanjanje Flatpak aplikacija počinje **nakon što se ponovo prijaviš u sustav**.

### Modus sinkronizacije

U modusu sinkronizacije se Flatpak aplikacije obrađuju **odmah nakon završetka sinkronizacije** (ponovno prijavljivanje nije potrebno).

## Važna napomena

Ako je opcija **Zadrži instalirane Flatpak aplikacije i podatke** deaktivirana, a imaš instalirane Flatpak aplikacije koje nisu uključene u uvezenu arhivu, one će se **trajno ukloniti zajedno sa svojim korisničkim podacima**.

{% include footer.html %}