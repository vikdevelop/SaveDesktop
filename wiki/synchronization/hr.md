# Sinkronizacija između računala u mreži

Osim spremanja konfiguracije i uvoza, Save Desktop također omogućuje sinkronizaciju između računala na tvojoj mreži pomoću mape za dijeljenje u oblaku ili Syncthing mape za dijeljenje.

## Postavljanje na prvom računalu
1. Otvori stranicu **Sinkroniziraj** u aplikaciji Save Desktop.
2. Klikni **„Postavi datoteku za sinkronizaciju.“**
3. Pojavit će se čarobnjak za brzo postavljanje:
   * Ako koristiš GNOME, Cinnamon, Budgie ili stariji COSMIC, koristi se metoda **GNOME Online Accounts**.
   * Za KDE Plasma ili druge radne površine, prebacuje se na **Rclone** (moraš samo kopirati naredbu i zalijepiti je u terminal).
   * Alternativno, možeš koristiti **Syncthing** klikom na **„Umjesto toga koristi Syncthing mapu“** i biranjem sinkronizirane mape.
4. Nakon što je čarobnjak gotov, otvorit će se dijalog **"Postavi datoteku za sinkronizaciju"**:
   * **Datoteka za periodično spremanje** (arhiva konfiguracije tvoje radne površine) počet će se generirati unutar odabrane mape.
   * Po želji možeš promijeniti interval ili ime datoteke pomoću gumba **„Promijeni“**.
5. Klikni **„Primijeni“**:
   * U istoj mapi se stvara jedna druga datoteka, „SaveDesktop.json“. Sadrži ime datoteke za sinkronizaciju i interval spremanja.
   * Dobit ćeš upit da se **odjaviš** iz svoje sesije kako bi se sinkronizacija mogla u potpunosti aktivirati.

## Povezivanje na drugo računalo
1. Na drugom računalu idi ponovo na stranicu **Sinkronizacija**.
2. Klikni **„Poveži se sa spremištem u oblaku.“**
3. Pojavit će se isti čarobnjak – odaberi mapu za sinkronizaciju putem GNOME OA, Rclone ili Syncthing.
4. Nakon čarobnjaka:
   * Otvara se dijaloh **„Poveži se sa spremištem u oblaku“**.
   * Odaberi **Interval sinkronizacije** i uključi ili isključi opdiju **Dvosmjerna sinkronizacija**.
5. Klikni **„Primijeni“**:
   * Dobit ćeš upit da se **odjaviš** ili ćeš (ako koristiš ručnu sinkronizaciju) dobiti obavijest da možeš sinkronizirati putem izbornika zaglavlja aplikacije.
   * Nakon ponovne prijave, Save Desktop se povezuje sa dijeljenom mapom i automatski sinkronizira tvoju konfiguraciju, s jednom obavijesti na početku i na kraju.

### Dvosmjerna sinkronizacija
Ako je **Dvosmjerna sinkronizacija** uključena na oba računala:
* Spremi postavke sinkronizacije kopija radne površine (kao što su interval i ime datoteke) s jednog uređaja na drugi,
* To održava sustave sinkroniziranima bez potrebe za ručnim konfiguriranjem oba uređaja.

## Datoteke koje se koriste u sinkronizaciji
* **Datoteka periodičnog spremanja** – '.sd.zip' arhiva tvoje konfiguracije radne površine, koja se redovito aktualizira.
* **SaveDesktop.json** – mala pomoćna datoteka koja spremaime datoteke arhive i interval spremanja, koja se koristi tijekom postavljanja sinkronizacije.

{% include footer.html %}