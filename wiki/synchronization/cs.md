
# Synchronizace mezi počítači v síti
#### Požadavky
- Na každém počítači, který chcete synchronizovat, musíte mít vytvořenou složku, která se bude synchronizovat s cloudovým úložištěm. To lze provést pomocí:
  
  <details>
    <summary><b>Online účty GNOME</b><p>(pro prostředí GNOME, Cinnamon, COSMIC (Old) a Budgie)</p></summary>
    <ul>
      <li>Otevřete Nastavení prostředí GNOME</li>
      <li>Přejděte do části Online účty a vyberte službu cloudového disku</li>
    </ul>
    <img src="https://raw.githubusercontent.com/vikdevelop/SaveDesktop/webpage/wiki/synchronization/screenshots/OnlineAccounts_en.png">
    
  </details>

  <details>
    <summary><b>Rclone</b><p>(pro jiná desktopová prostředí)</p></summary>
    <ul>
      <li>Nainstalujte Rclone</li>
      <pre><code>sudo -v ; curl https://rclone.org/install.sh | sudo bash</code></pre>
      <li>Nastavte Rclone pomocí tohoto příkazu, který vytvoří složku cloudové jednotky, nastaví Rclone a připojí složku
      <pre><code>mkdir -p ~/drive &amp;&amp; rclone config create drive your-cloud-drive-service &amp;&amp; nohup rclone mount drive: ~/drive --vfs-cache-mode writes &amp; echo "The drive has been mounted successfully"</code></pre>
      <p>* Namísto `your-cloud-drive-service` použijte název služby cloudového disku, například `drive` (pro Google Drive), `onedrive`, `dropbox` atd.</p></li>
      <li>Povolte přístup k vytvořené složce v aplikaci [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal).</li>
    </ul>
  </details>
  
## Nastavení synchronizace v aplikaci SaveDesktop
V prvním počítači:
1. Otevřete aplikaci SaveDesktop
2. Na stránce Synchronizace klikněte na tlačítko „Nastavit synchronizační soubor“ a poté na tlačítko „Změnit“. 3. Klikněte na tlačítko „Nastavit synchronizační soubor“.
3. Klikněte na možnost „Periodické ukládání“ a vyberte složku, která je synchronizována s cloudovým úložištěm, jako složku pro pravidelné ukládání.
4. Pokud soubor pro pravidelné ukládání neexistuje, klikněte na tlačítko Vytvořit

V druhém počítači:
1. Otevřete aplikaci SaveDesktop
2. Přejděte na stránku Synchronizace a klikněte na tlačítko „Připojit ke cloudovému úložišti“.
3. Klikněte na tlačítko „Select cloud drive folder“ (Vybrat složku cloudové jednotky) a vyberte složku, která je synchronizována se stejným cloudovým úložištěm jako první počítač.
4. Vyberte interval pravidelné synchronizace, protože pokud ponecháte hodnotu Nikdy, synchronizace nebude fungovat.

Chcete-li nastavit obousměrnou synchronizaci, ujistěte se, že máte v dialogovém okně „Připojit ke cloudovému úložišti“ na prvním počítači vybranou stejnou složku cloudového úložiště, zvolený interval periodické synchronizace a povolený přepínač „Obousměrná synchronizace“.

### Pravidelná synchronizace
Můžete si vybrat mezi následujícími možnostmi:
- Denně
- Týdně (synchronizace probíhá každé úterý)
- Měsíčně (synchronizace probíhá každý druhý den v měsíci)
- Ručně (je možné synchronizovat konfiguraci z menu v záhlaví kliknutím na tři tečky)
- Nikdy (nic se neděje)

{% include footer.html %}
