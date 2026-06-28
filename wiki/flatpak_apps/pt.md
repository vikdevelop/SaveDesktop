# Guardar, importar e sincronizar aplicações Flatpak

O Save Desktop permite guardar, importar e sincronizar aplicações Flatpak juntamente com os respetivos dados de utilizador, além de ícones, temas, definições e extensões.

## Onde posso encontrar isto?

As opções relacionadas com Flatpak encontram-se na janela **Selecionar itens da configuração**.
Podes abri-la a partir do menu da barra de cabeçalho (três pontos na barra de título da janela).

## Opções disponíveis

### Lista de aplicações Flatpak instaladas

Guarda e restaura a lista de aplicações Flatpak instaladas.

### Dados de utilizador das aplicações Flatpak instaladas

Permite incluir os dados de utilizador das aplicações Flatpak selecionadas.
Clica no botão **">"** para escolher as aplicações cujos dados devem ser guardados.

### Manter aplicações e dados Flatpak instalados (ativo por predefinição)

Quando esta opção está ativa, o Save Desktop **NÃO remove aplicações Flatpak nem os respetivos dados que não estejam presentes no arquivo**.

Quando está desativada, o Save Desktop **remove qualquer aplicação Flatpak instalada que não esteja listada no arquivo importado — incluindo os respetivos dados de utilizador**.

⚠️ **Aviso:**
Desativa esta opção apenas se quiseres que o teu sistema corresponda exatamente ao arquivo importado. As aplicações removidas e os respetivos dados **não podem ser recuperados**.

## Como funciona a importação?

Depois de selecionares um arquivo ou uma pasta, ser-te-á pedido que escolhas os itens da configuração a importar.
Clica em **Aplicar** para iniciar o processo de importação.

Ordem de importação:

1. Configuração do ambiente de trabalho (ícones, temas, tipos de letra, extensões, definições, etc.)
2. Aplicações Flatpak e respetivos dados de utilizador (após o próximo início de sessão)

A instalação e remoção de aplicações Flatpak começam **depois de voltares a iniciar sessão no sistema**.

### Modo de sincronização

No modo de sincronização, as aplicações Flatpak são processadas **imediatamente após a conclusão da sincronização** (sem ser necessário voltar a iniciar sessão).

## Nota importante

Se **Manter aplicações e dados Flatpak instalados** estiver desativado e tiveres aplicações Flatpak instaladas que não estejam incluídas no arquivo importado, estas serão **removidas permanentemente juntamente com os respetivos dados de utilizador**.

{% include footer.html %}