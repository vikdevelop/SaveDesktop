# Guardar Periodicamente
Além de guardar manualmente,o  SaveDesktop permite-te também guardares a tua configuração de desktop periodicamente. Podes escolher uma das seguintes opções:
- **Diariamente**: 
  - Depois de fazeres login, o SaveDesktop irá iniciar no fundo e guardará a configuração. Se voltares a fazer login no mesmo dia, não o voltará a fazer porque já foi executado uma vez no dia.
- **Semanalmente**:
  - O SaveDesktop cria uma cópia das configurações todas as Segunda-feira se "Semanalmente" estiver seleccionado. Se o computador não estiver a correr nesse dia, o SaveDesktop não o fará no dia seguinte.
- **Mensalmente**:
  - Se "Mensalmente" for selecionado, o SaveDesktop faz uma cópia no primeiro dia do mês, ex. 1 Maio, 1 Junho, 1 Dezembro, etc. Tal como "Semanalmente", se o computador não estiver a correr nesse dia, o SaveDesktop não o fará no dia seguinte.
- **Nunca**:
  - Nada acontece

### Where are the periodic saving files stored?
Default directory for periodic saving is `/home/user/Downloads/SaveDesktop/archives`, but you can choose custom directory.

### Filename format
If you want to give a filename format for periodic saving files other than `Latest_configuration`, it is possible, even with spaces. Since version 2.9.6, variable `{}` doesn't work for setting the today date because now, in every periodic saving, the original backup file is overwritten.

_If you have any questions, you can use Github issues._
