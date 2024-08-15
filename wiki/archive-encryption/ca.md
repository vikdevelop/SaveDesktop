# Xifrat del fitxer
**Aquesta característica és disponible des de la versió: 3.3**

Si, per raons de seguretat o qualsevol altre motiu, voleu xifrar el fitxer de configuració, podeu utilitzar la característica inclosa al SaveDesktop. Com es fa, llavors?

## Com funciona?
En habilitar aquesta característica, el SaveDesktop us demanarà sempre crear-ne una contrasenya per als fitxers de configuració nous que es generin. Perquè la contrasenya sigui forta, ha de tenir almenys 12 caràcters, contenir una majúscula i una minúscula, a més d'un caràcter especial. Si la contrasenya no compleix aquests requisits, no serà possible continuar desant la configuració.

The archive will be saved as a ZIP El fitxer es desarà com a format ZIP (perquè un Tar no suporta protecció per contrasenya) i, en intentar extreure el seu contingut, si us demanarà la contrasenya que vau utilitzar durant el procés de creació. També si us demanarà quan vulgueu importar-ne la configuració.

Si oblideu la contrasenya, no serà possible de cap manera extreure el contingut o importar cap configuració continguda al fitxer.

> [!ATENCIÓ]
> El desament periòdic crea sempre fitxers sense contrasenya. Els fitxers xifrats no es poden emprar en tasques de sincronització.

## Com es configura?
A partir de la versió 3.3, la interfície ha canviat significativament, en concret la secció del desament periòdic que ara es troba al botó «Més opcions». Al mateix lloc, es troba la secció de xifratge. Feu clic al botó esmenat i habiliteu l'opció Xifrat del fitxer.



{% include footer.html %}
