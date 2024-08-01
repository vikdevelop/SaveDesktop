# Salvamento Periódico
Além dos salvamentos manuais, o SaveDesktop também permite que você salve sua configuração de desktop periodicamente. Você pode escolher entre as seguintes opções:
- **Diariamente**: 
  - Após logar no sistema, o SaveDesktop é iniciado em segundo plano e faz um backup da sua configuração. Se você logar novamente no mesmo dia, o app não fará o backup novamente, pois ele já terá sido feito para aquele dia.
- **Semanalmente**:
  - O SaveDesktop faz um backup da configuração toda segunda-feira, se a opção "Semanalmente" estiver selecionada. Se o computador não estiver funcionando naquele dia, o SaveDesktop não realiza o backup no próximo dia.
- **Mensalmente**:
  - Se a opção "Mensalmente" estiver selecionada, o SaveDesktop faz o backup no primeiro dia do mês — por exemplo, 1º de maio, 1º de junho, 1º de dezembro, etc. Assim como na opção "Semanalmente", se o computador não estiver funcionando naquele dia, o SaveDesktop não realiza o backup no próximo dia.
- **Nunca**:
  - Nada acontece

### Onde os arquivos de salvamento periódico são armazenados?
O diretório padrão para o salvamento periódico é `/home/user/Downloads/SaveDesktop/archives`, mas você pode escolher um diretório personalizado.

### Formato do nome do arquivo
Se você deseja definir um formato de nome de arquivo para arquivos de salvamento periódico diferente de `Latest_configuration`, isso é possível, até mesmo com espaços. Desde a versão 2.9.6, a variável `{}` não funciona para inserir a data atual porque agora, em todo salvamento periódico, o arquivo de backup original é sobrescrito.

_Se você tiver quaisquer questões, pode usar as issues do GitHub._

{% include footer.html %}
