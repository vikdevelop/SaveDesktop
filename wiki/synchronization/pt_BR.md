# Sincronização entre computadores na rede
#### Requisitos
- Você deve criar uma pasta que será sincronizada com seu armazenamento em nuvem em cada computador que deseja sincronizar. Isso pode ser feito usando:

  <details>
    <summary> <b> Contas on -line gnome </b> <p> (para ambientes Gnome, Cinnamon, Cosmic (antigo) e de desktop) </p> </summary>
    <ul>
        <li> Abra as configurações do Gnome </li>
        <li> Vá para a seção de contas on -line e selecione seu serviço de unidade de nuvem </li>
    </ul>
    <img src="https://raw.githubusercontent.com/vikdevelop/SaveDesktop/webpage/wiki/synchronization/screenshots/OnlineAccounts_en.png">
    
  </details>

  <details>
    <summary><b>Rclone</b><p>(para outros ambientes de mesa)</p></summary>
    <ul>
      <li>Instale o rclone</li>
      <pre><code>sudo -v ; curl https://rclone.org/install.sh | sudo bash</code></pre>
      <li>Configure o RCLONE usando este comando, que cria a pasta de unidade de nuvem, configura Rclone e monta a pasta</li>
      <pre><code>mkdir -p ~/Downloads/SaveDesktop/rclone_drive &amp;&amp; rclone config create savedesktop your-cloud-drive-service &amp;&amp; nohup rclone mount savedesktop: ~/Downloads/SaveDesktop/rclone_drive --vfs-cache-mode writes &amp; echo "a unidade foi montada com sucesso"</code></pre>
      <p>* Em vez de <code>your-cloud-drive-service</code> use o nome do seu serviço de unidade em nuvem, como <code>drive</code> (para o Google Drive), <code>onedrive</code>, <code>dropbox</code>, etc.</p></li>
    </ul>
  </details>
  
## Configurando a sincronização no aplicativo SaveDesktop
No primeiro computador:
1. Abra o aplicativo SaveDesktop
2. Na página Sincronizar, clique no botão "Configurar o arquivo de sincronização" e depois no botão "Alterar"
3. Clique em "Salvamento periódico" e selecione a pasta que está sincronizada com seu armazenamento em nuvem como uma pasta de salvamento periódico
4. Caso o arquivo de salvamento periódico não exista, clique no botão Criar

No segundo computador:
1. Abra o aplicativo SaveDesktop
2. Vá para a página Sincronizar e clique no botão "Conectar ao armazenamento em nuvem".
3. Clique no botão "Selecionar pasta da unidade em nuvem" e selecione a pasta que está sincronizada com o mesmo armazenamento em nuvem do primeiro computador.
4. Selecione o intervalo de sincronização periódica, pois se deixar como Nunca a sincronização não funciona.

Para configurar a sincronização bidirecional, certifique-se de ter a mesma pasta de nuvem selecionada na caixa de diálogo "Conectar ao armazenamento em nuvem" no primeiro computador, o intervalo de sincronização periódica selecionado e a opção "Sincronização bidirecional" ativada.

## Sincronização periódica
Você pode escolher entre as seguintes opções:
- Diariamente
- Semanalmente
- Mensalmente
- Manualmente (é possível sincronizar a configuração a partir do menu na barra de cabeçalho, clicando nos três pontos)
- Nunca (nada acontece)

{% include footer.html %}

