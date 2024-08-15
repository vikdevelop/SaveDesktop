# Sincronização entre computadores na rede
## Como configurar?
### Quais as suas necessidades?</str>

**No computador 1:**
- atribua manualmente o endereço IP dos seus dispositivos que você deseja sincronizar de modo que o endereço IP deles não mude toda ver que o computador for ligado. É possível definir isso por meio de:

  **Configurações do roteador:**

  - [para roteadores Asus](https://www.asus.com/support/FAQ/1000906/)
  - [para roteadores Tp-link](https://www.tp-link.com/us/support/faq/170/)
  - [para roteadores Tenda](https://www.tendacn.com/faq/3264.html)
  - [para roteadores Netgear](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - se você não tiver um dos roteadores acima, abra as configurações do seu roteador (URL: [192.168.1.1](http://192.168.1.1) ou similar) e busque na seção de servidor DHCP por algo como "Atribuir manualmente um IP para a lista DHCP" ou "IP Estático", etc.

  **pacote `system-config-printer`:**  <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
  
  - se você não quiser atribuir o endereço de IP manualmente por meio da interface do roteador, e tiver uma impressora e tiver instalado o pacote `system-config-printer`, confira se você marcou a opção "Compartilhada" clicando na aba Impressora na barra de cabeçalho. Se não, por favor marque e reinicie o sistema. [Aqui](https://github-production-user-asset-6210df.s3.amazonaws.com/83600218/272054218-ff17c19b-98f5-41fe-8f34-40de275f0da4.png) está uma captura de tela mostrando como deve estar.

**No computador 2:**
- Confira se você está conectado na mesma rede que o computador 1.

### Definir sincronização no aplicativo SaveDesktop

<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

Nos computadores 1 e 2, abra o aplicativo SaveDesktop e mude para a página Sincronizar. No computador 1, clique no botão "Configurar o arquivo de sincronização", escolha o arquivo de sincronização (seu arquivo de salvamento periódico), e escolha um intervalo de sincronização periódica. Então copie a URL para sincronização e, no computador 2, clique no botão "Conectar-se com outro computador" e insira a URL para sincronização copiada do computador 1.
 
Se você deseja sincronizar a configuração de ambiente de área de trabalho do computador 2 para o computador 1, realize o mesmo procedimento.

**Para que as alterações tenham efeito, é necessário encerrar a sessão no sistema**

## Sincronização periódica
Você pode escolher entre as seguintes opções:
- Diariamente
- Semanalmente (a sincronização acontece toda terça-feira)
- Mensalmente (a sincronização acontece todo segundo dia do mês)
- Manualmente (é possível sincronizar a configuração a partir do menu na barra de cabeçalho, clicando nos três pontos)
- Nunca (nada acontece)



{% include footer.html %}
