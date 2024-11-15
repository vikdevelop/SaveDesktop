# Sincronização entre computadores na rede
#### Requisitos
- Você deve criar uma pasta que será sincronizada com seu armazenamento em nuvem em cada computador que deseja sincronizar. Isso pode ser feito usando:

  <details>
    <summary><b>GNOME Online Accounts</b><p>(for GNOME, Cinnamon, COSMIC (Old) and Budgie desktop environments)</p></summary>
    <ul>
      <li>Open the GNOME Settings</li>
      <li>Go to the Online Accounts section and select your cloud drive service</li>
    </ul>
    <img src="https://raw.githubusercontent.com/vikdevelop/SaveDesktop/webpage/wiki/synchronization/screenshots/OnlineAccounts_en.png">
    
  </details>

  <details>
    <summary><b>Rclone</b><p>(for other desktop environments)</p></summary>
    <ul>
      <li>Install Rclone</li>
      <pre><code>sudo -v ; curl https://rclone.org/install.sh | sudo bash</code></pre>
      <li>Setup Rclone by using this command, which creates the cloud drive folder, sets up Rclone and mounts the folder
      <pre><code>mkdir -p ~/drive &amp;&amp; rclone config create drive your-cloud-drive-service &amp;&amp; nohup rclone mount drive: ~/drive --vfs-cache-mode writes &amp; echo "The drive has been mounted successfully"</code></pre>
      <p>* Instead of `your-cloud-drive-service` use the name of your cloud drive service, such as `drive` (for Google Drive), `onedrive`, `dropbox`, etc.</p></li>
      <li>Allow access to the created folder in the [Flatseal app](https://flathub.org/apps/com.github.tchx84.Flatseal).</li>
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
- Semanalmente (a sincronização acontece toda terça-feira)
- Mensalmente (a sincronização acontece todo segundo dia do mês)
- Manualmente (é possível sincronizar a configuração a partir do menu na barra de cabeçalho, clicando nos três pontos)
- Nunca (nada acontece)

{% include footer.html %}

