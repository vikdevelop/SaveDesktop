
# नेटवर्क में कंप्यूटरों के बीच समन्वयन
## Requirements
- You must have a folder created that will sync with your cloud storage on each computer you want to sync. This can be done using:

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
  
## Setting up synchronization in the SaveDesktop app
On the first computer:
1. Open the SaveDesktop app
2. On the Sync page, click on the "Set up the sync file" button and then on the "Change" button
3. Click on "Periodic saving" and select the folder that is synchronized with your cloud storage as a periodic saving folder
4. If the periodic saving file does not exist, click on the Create button

On the second computer:
1. Open the SaveDesktop app
2. Go to the Sync page and click the "Connect to the cloud storage" button.
3. Click on the "Select cloud drive folder" button and select the folder that is synced with the same cloud storage as the first computer.
4. Select the periodic synchronization interval, because if you leave that to Never, the synchronization doesn't work.

To set up bidirectional synchronization, make sure you have the same cloud folder selected in the "Connect to cloud storage" dialog on the first computer, the periodic synchronization interval selected, and the "Bidirectional synchronization" switch enabled.

### Periodic synchronization
You can choose between the following options:
- Daily
- Weekly 
- Monthly 
- Manually (it is possible to sync configuration from the menu in the header bar by clicking on the three dots)
- Never (nothing's happening)

{% include footer.html %}
