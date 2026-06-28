# Sincronização entre computadores na rede

Além de guardar e importar a configuração, o Save Desktop também permite sincronizá-la entre computadores na tua rede através de uma pasta partilhada na nuvem ou de uma pasta partilhada do Syncthing.

## Configuração no primeiro computador
1. Abre a página **Sincronizar** na aplicação Save Desktop.
2. Clica em **"Configurar o ficheiro de sincronização"**.
3. Será apresentado um assistente de configuração rápida:
   * Se usares GNOME, Cinnamon, Budgie ou uma versão antiga do COSMIC, será usado o método **Contas online do GNOME**.
   * No KDE Plasma ou noutros ambientes de trabalho, será usado o **Rclone** (só terás de copiar um comando e colá-lo no terminal).
   * Em alternativa, podes usar o **Syncthing** clicando em **"Usar uma pasta do Syncthing em alternativa"** e selecionando uma pasta sincronizada.
4. Depois de concluíres o assistente, será aberta a janela **"Configurar o ficheiro de sincronização"**:
   * Um **ficheiro de cópia de segurança periódica** (o arquivo de configuração do teu ambiente de trabalho) começará a ser gerado dentro da pasta selecionada.
   * Opcionalmente, podes alterar o intervalo ou o nome do ficheiro com o botão **"Alterar"**.
5. Clica em **"Aplicar"**:
   * Um segundo ficheiro, `SaveDesktop.json`, é criado na mesma pasta. Contém o nome do ficheiro de sincronização e o intervalo de cópia de segurança.
   * Ser-te-á pedido que **termines sessão** para que a sincronização possa ser totalmente ativada.

## Ligar noutro computador
1. No outro computador, volta à página **Sincronizar**.
2. Clica em **"Ligar ao armazenamento na nuvem"**.
3. Será apresentado o mesmo assistente — escolhe a tua pasta sincronizada através das Contas online do GNOME, Rclone ou Syncthing.
4. Depois do assistente:
   * A janela **"Ligar ao armazenamento na nuvem"** é aberta.
   * Seleciona o **intervalo de sincronização** e ativa ou desativa a **Sincronização bidirecional**.
5. Clica em **"Aplicar"**:
   * Ser-te-á pedido que **termines sessão** ou, se usares a sincronização manual, serás informado de que podes sincronizar a partir do menu da barra de cabeçalho da aplicação.
   * Depois de voltares a iniciar sessão, o Save Desktop liga-se à pasta partilhada e sincroniza automaticamente a tua configuração, com uma notificação no início e no fim.

### Sincronização bidirecional
Se a **Sincronização bidirecional** estiver ativa em ambos os computadores:
* O Save Desktop copia as definições de sincronização (como o intervalo e o nome do arquivo) de uma máquina para a outra;
* Isto mantém os sistemas sincronizados sem ser necessário configurar cada um manualmente.

## Ficheiros usados na sincronização
* **Ficheiro de cópia de segurança periódica** — um arquivo `.sd.zip` da configuração do teu ambiente de trabalho, atualizado regularmente.
* **SaveDesktop.json** — um pequeno ficheiro auxiliar que guarda o nome do arquivo e o intervalo de cópia de segurança, usado durante a configuração da sincronização.

{% include footer.html %}