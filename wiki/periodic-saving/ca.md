# Desament automàtic
A més de les còpies manuals, el SaveDesktop també us permet automatitzar aquest procés. Podeu triar entre aquestes opcions disponibles:
- **Diàriament**: 
  - Després d'iniciar la sessió al sistema, el SaveDesktop crea una còpia en rerefons de la configuració. Si torneu a iniciar la sessió, no crearà cap còpia atès que ja existeix una del mateix dia.
- **Setmanalment**:
  - El SaveDesktop crea una còpia de seguretat de la configuració cada dilluns en seleccionar aquest mode. Si no engegueu l'ordinador aquest dia, el SaveDesktop no en crearà cap còpia fins al dilluns següent.
- **Mensualment**:
  - En seleccionar aquest mode, el SaveDesktop crea una còpia el primer dia 1 del mes (p. ex. 1 d'octubre, 1 de novembre, etc.) i, de la mateixa forma que amb la còpia setmanal, si l'equip no està funcionant en aquest dia, no farà cap còpia fins al proper dia 1 del mes vinent.
- **Mai**:
  - No es crea cap còpia automàtica

### On es desen els fitxers de còpia automàtica?
La carpeta per defecte d'emmagatzematge és `/home/user/Baixades/SaveDesktop/archives`, però podeu triar una ruta personalitzada.

### Format del nom de fitxer
Si voleu crear còpies automàtiques amb altre nom diferent a `Darreraconfiguració`, ja és possible, fins i tot amb espais. Des de la versió 2.9.6, la variable `{}` no s'admet per al dia actual, atès que ara totes les còpies automàtiques sobreescriuen el fitxer ja existent.



{% include footer.html %}
