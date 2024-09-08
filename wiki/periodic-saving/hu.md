
# Időszakos mentés
A manuális mentések mellett, a SaveDesktop lehetővé teszi, hogy időszakosan elmentsd a számítógéped beállításait. A következő lehetőségek közül választhatsz:
- **Naponta**: 
  - Bejelentkezés után a SaveDesktop elindul a háttérben és elmenti a beállításokat. Ha ugyanazon a napon újra belépsz, a mentés nem fut le még egyszer, hiszen arra a napra már készült biztonsági mentés.
- **Hetente**:
  - A SaveDesktop minden hétfőn biztonsági mentést készít. Ha a számítógép nem fut azon a napon, a SaveDesktop nem készít mentést a következő napon.
- **Havonta**:
  - A SaveDesktop a hónap első napján készíti el a biztonsági mentést. Például, május elsején, június elsején, december elsején, stb. Hasonlóan a heti mentéshez, ha a számítógép nem fut az adott napon, az alkalmazás nem készíti el a mentést a következőn.
- **Soha**:
  - Semmi sem történik.

### Hol tárolódnak a biztonsági mentések?
Az időszakos mentések alapértelmezett könyvtára a `/home/user/Letöltések/SaveDesktop/archives`, de választhatsz egyéni könyvtárat is.

### Fájlnév formátum
If you want to give a filename format for periodic saving files other than `Latest_configuration`, it is possible, even with spaces. Since version 2.9.6, variable `{}` doesn't work for setting the today date because now, in every periodic saving, the original backup file is overwritten.



{% include footer.html %}
