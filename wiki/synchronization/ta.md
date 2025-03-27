# நெட்வொர்க்கில் கணினிகளுக்கு இடையே ஒத்திசைவு
#### தேவைகள்
 - நீங்கள் ஒத்திசைக்க விரும்பும் ஒவ்வொரு கணினியிலும் உங்கள் மேகக்கணி சேமிப்பகத்துடன் ஒத்திசைக்கும் ஒரு கோப்புறை உருவாக்கப்பட வேண்டும். இதைப் பயன்படுத்தி செய்ய முடியும்:

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
          <pre><code>mkdir -p ~/Downloads/SaveDesktop/rclone_drive &amp;&amp; rclone config create savedesktop your-cloud-drive-service &amp;&amp; nohup rclone mount savedesktop: ~/Downloads/SaveDesktop/rclone_drive --vfs-cache-mode writes &amp; echo "The drive has been mounted successfully"</code></pre>
          <p>* Instead of <code>your-cloud-drive-service</code> use the name of your cloud drive service, such as <code>drive</code> (for Google Drive), <code>onedrive</code>, <code>dropbox</code>, etc.</p></li>
        </ul>
      </details>

## savedesktop பயன்பாட்டில் ஒத்திசைவை அமைத்தல்
 முதல் கணினியில்:
 1. savedesktop பயன்பாட்டைத் திறக்கவும்
 2. ஒத்திசைவு பக்கத்தில், "ஒத்திசைவு கோப்பை அமைக்கவும்" பொத்தானைக் சொடுக்கு செய்து, பின்னர் "மாற்று" பொத்தானைக் சொடுக்கு செய்க
 3. "அவ்வப்போது சேமிப்பு" என்பதைக் சொடுக்கு செய்து, உங்கள் முகில் சேமிப்பகத்துடன் ஒத்திசைக்கப்பட்ட கோப்புறையைத் தேர்ந்தெடுக்கவும், அவ்வப்போது சேமிக்கும் கோப்புறையாக
 4. அவ்வப்போது சேமிக்கும் கோப்பு இல்லை என்றால், உருவாக்கு பொத்தானைக் சொடுக்கு செய்க

இரண்டாவது கணினியில்:
 1. savedesktop பயன்பாட்டைத் திறக்கவும்
 2. ஒத்திசைவு பக்கத்திற்குச் சென்று "முகில் ச்டோரேச் உடன் இணைக்கவும்" பொத்தானைக் சொடுக்கு செய்க.
 3. "முகில் இயக்கி கோப்புறையைத் தேர்ந்தெடுக்கவும்" பொத்தானைக் சொடுக்கு செய்து, முதல் கணினியின் அதே முகில் சேமிப்பகத்துடன் ஒத்திசைக்கப்பட்ட கோப்புறையைத் தேர்ந்தெடுக்கவும்.
 4. அவ்வப்போது ஒத்திசைவு இடைவெளியைத் தேர்ந்தெடுக்கவும், ஏனென்றால் நீங்கள் அதை ஒருபோதும் விட்டுவிட்டால், ஒத்திசைவு வேலை செய்யாது.

இருதரப்பு ஒத்திசைவை அமைக்க, முதல் கணினியில் "முகில் ச்டோரேச் உடன் இணைக்கவும்" உரையாடலில் அதே முகில் கோப்புறை, தேர்ந்தெடுக்கப்பட்ட கால ஒத்திசைவு இடைவெளி மற்றும் "இருதரப்பு ஒத்திசைவு" சுவிட்ச் இயக்கப்பட்டதா என்பதை உறுதிப்படுத்திக் கொள்ளுங்கள்.

### அவ்வப்போது ஒத்திசைவு
 பின்வரும் விருப்பங்களுக்கு இடையே நீங்கள் தேர்வு செய்யலாம்:
 - நாள்தோறும்
 - வாராந்திர
 - மாதாந்திர
 - கைமுறையாக (தலைப்பு பட்டியில் உள்ள மெனுவிலிருந்து உள்ளமைவை மூன்று புள்ளிகளைக் சொடுக்கு செய்வதன் மூலம் ஒத்திசைக்க முடியும்)
 - ஒருபோதும் (எதுவும் நடக்கவில்லை)

{% include footer.html %}
