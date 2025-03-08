# Sincronització entre ordinadors de la xarxa
#### Requisits
- Heu de crear prèviament una carpeta que sincronitzi amb el vostre emmagatzematge al núvol i que sigui disponible a cada ordinador que voleu aplicar la sincronització. Es pot dur a terme utilitzant:

  <details>
    <summary><b>Comptes en línia del GNOME</b><p>(per a entorns d'escriptori GNOME, Cinnamon, COSMIC (obsolet) i Budgie)</p></summary>
    <ul>
      <li>Obriu la configuració del GNOME</li>
      <li>Aneu a la secció dels comptes en línia i trieu el servei al núvol de la vostra preferència</li>
    </ul>
    <img src="https://raw.githubusercontent.com/vikdevelop/SaveDesktop/webpage/wiki/synchronization/screenshots/OnlineAccounts_en.png">
    
  </details>

  <details>
    <summary><b>Rclone</b><p>(per a altres entorns d'escriptori)</p></summary>
    <ul>
      <li>Instal·leu el Rclone</li>
      <pre><code>sudo -v ; curl https://rclone.org/install.sh | sudo bash</code></pre>
      <li>Utilitzeu aquesta ordre que crearà la carpeta al núvol, configura el Rclone i munta la carpeta
      <pre><code>mkdir -p ~/Downloads/SaveDesktop/rclone_drive &amp;&amp; rclone config create savedesktop your-cloud-drive-service &amp;&amp; nohup rclone mount savedesktop: ~/Downloads/SaveDesktop/rclone_drive --vfs-cache-mode writes &amp; echo "S'ha muntat la unitat correctament"</code></pre>
      <p>* En comptes d'  <code>el-vostre-servei-al-núvol</code> indiqueu el nom del proveïdor de serveis, com ara <code>drive</code> (per al Google Drive), <code>onedrive</code>, <code>dropbox</code>, etc.</p></li>
    </ul>
  </details>
  
## Configuració de la sincronització a l'aplicació SaveDesktop
Al primer ordinador:
1. Obriu l'aplicació SaveDesktop
2. A la pàgina de sincronització, feu clic al botó «Configura el fitxer de sincronització» i després al botó «Canvia»
3. Feu clic a «Desat periòdic» i seleccioneu la carpeta que sincronitza amb l'emmagatzematge al núvol com a carpeta de desat periòdic
4. Si el fitxer de configuració no existeix, feu clic al botó «Crea»

Al segon ordinador:
1. Inicieu el SaveDesktop
2. Aneu a la pàgina de sincronització i feu clic al botó «Connecta amb l'emmagatzematge al núvol».
3. Feu clic al botó «Selecciona la carpeta al núvol» i trieu la carpeta del mateix emmagatzematge al núvol que té el primer ordinador.
4. Seleccioneu la periodicitat de la sincronització perquè, si ho deixeu en blanc, la sincronització no funcionarà.

Per a configurar una sincronització bidireccional, assegureu-vos que teniu configurada la mateixa carpeta de l'apartat «Connectat amb l'emmagatzematge al núvol» del primer ordinador, que existeix un interval de sincronització periòdica seleccionat i que està habilitada l'opció «Sincronització bidireccional».

## Sincronització periòdica
Podeu triar entre les opcions següents:
- Diàriament
- Setmanalment
- Mensualment
- Manualment (és possible realitzar la sincronització en qualsevol moment des del menú principal en fer clic als tres punts)
- Mai (no es duu a terme cap canvi)

{% include footer.html %}
