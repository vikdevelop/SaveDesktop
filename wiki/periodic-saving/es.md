# Guardado automático
Además de los guardados manuales, SaveDesktop también le permite guardar regularmente la configuración de su escritorio. Puede elegir entre las siguientes opciones:
- **Diariamente**: 
  - Después de iniciar la sesión en el sistema, SaveDesktop se inicia en segundo plano y realiza una copia de seguridad de la configuración. Si vuelve a iniciar sesión ese mismo día, no volverá a hacerlo, porque ya se ha creado para ese día.
- **Semanalmente**:
  - SaveDesktop realiza una copia de seguridad de la configuración cada lunes si se selecciona "Semanalmente". Si el ordenador no está funcionando ese día, SaveDesktop la hará al día siguiente.
- **Mensualmente**:
  - Si se selecciona "Mensual", SaveDesktop realiza la copia de seguridad el primer día del mes, por ejemplo, el 1 de mayo, el 1 de junio, el 1 de diciembre, etc. Al igual que con "Semanal", si el ordenador no está funcionando ese día, SaveDesktop no la realiza al día siguiente.
- **Nunca**:
  - No ocurre nada

### ¿Dónde se almacenan los archivos de guardado periódicamente?
El directorio por defecto para guardar los periódicamente es `/home/user/Downloads/SaveDesktop/archives`, pero puede elegir un directorio personalizado.

### Formato del archivo
Si desea crear copias automáticas con otro nombre diferente a `Última_configuración`, ya es posible, incluso con espacios. Desde la versión 2.9.6, la variable `{}` no se admite para el día actual, dado que ahora todas las copias automáticas sobrescriben el archivo ya existente.



{% include footer.html %}
