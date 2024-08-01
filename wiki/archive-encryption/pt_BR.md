# Encriptação de arquivo
**Essa funcionalidade está disponível a partir da versão: `3.3`**

Se você deseja encriptar o arquivo de configuração, seja por razões de proteção dos dados ou qualquer outra coisa, você pode usar a funcionalidade de encriptação de arquivo do aplicativo SaveDesktop. Mas como ela funciona, e como configurá-la?

## Como funciona?
Se essa funcionalidade estiver ativada, o SaveDesktop sempre irá te pedir para criar uma senha para o seu novo arquivo de configuração. Os critérios para a senha incluem pelo menos 12 caracteres de tamanho, uma letra maiúscula, uma letra minúscula, e um caractere especial. Se a senha não atender esses critérios, não será possível continuar a salvar a configuração.

O arquivo será salvo como um arquivo ZIP (uma vez que o Tar não suporta a funcionalidade de proteção com senha) e, se você quiser extrai-lo, será pedido que você insira a senha que você definiu no processo de salvamento da configuração. O mesmo se aplica no caso de importação da configuração.

Se você esquecer a senha, não conseguirá extrair o arquivo e usá-lo no processo de importação da configuração.

> [!WARNING]  
> Os arquivos de salvamento periódico não estão (por ora) disponíveis para proteção com senha. Arquivos encriptados não podem, por ora, ser utilizados para sincronização.

## Como configurar?
Na versão 3.3, a interface foi levemente modificada; especificamente, a seção de salvamento periódico agora pode ser acessada através do botão "Mais opções". No mesmo local é possível encontrar a seção de encriptação de arquivo. Então clique no botão mencionado, e ative o interruptor de Encriptação de arquivo.

_Se você tiver quaisquer questões, pode usar as issues do GitHub._
{% include footer.html %}
