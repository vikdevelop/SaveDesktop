# नेटवर्क में कंप्यूटरों के बीच समन्वयन

In addition to saving the configuration and importing it, Save Desktop also allows you to synchronize it between computers on your network using a shared cloud folder or a shared Syncthing folder.

## Setting Up on the First Computer
1. Open the **Sync** page in the Save Desktop app.
2. Click **“Set up the sync file.”**
3. A quick setup wizard will appear:
   * If you're using GNOME, Cinnamon, Budgie, or older COSMIC, the **GNOME Online Accounts** method is used.
   * For KDE Plasma or other desktops, it switches to **Rclone** (you’ll just need to copy a command and paste it into the terminal).
   * Alternatively, you can use **Syncthing** by clicking **“Use Syncthing’s folder instead”** and selecting a synced folder.
4. After finishing the wizard, the **“Set up the sync file”** dialog will open:
   * A **periodic saving file** (your desktop config archive) will start generating inside the selected folder.
   * You can optionally change the interval or filename using the **“Change”** button.
5. Click **“Apply”**:
   * A second file, `SaveDesktop.json`, is created in the same folder. It contains the sync file name and saving interval.
   * You will be prompted to **log out** of your session so synchronization can fully activate.

## Connecting on Another Computer
1. On the other computer, go to the **Sync** page again.
2. Click **“Connect to the cloud storage.”**
3. The same wizard will appear – choose your synced folder via GNOME OA, Rclone, or Syncthing.
4. After the wizard:
   * The **“Connect to the cloud storage”** dialog opens.
   * Select the **sync interval** and enable or disable **Bidirectional synchronization**.
5. Click **“Apply”**:
   * You will be prompted to **log out**, or (if using manual sync) informed that you can sync from the app’s header menu.
   * After logging back in, Save Desktop connects to the shared folder and syncs your configuration automatically, with a notification at the start and end.

### Bidirectional Synchronization
If **Bidirectional synchronization** is enabled on both computers:
* Save Desktop copies sync settings (such as interval and filename) from one machine to the other,
* This keeps your systems in sync without needing to configure each one manually.

## Files Used in Synchronization
* **Periodic saving file** – a `.sd.zip` archive of your desktop configuration, updated regularly.
* **SaveDesktop.json** – a small helper file that stores the archive’s filename and saving interval, used during sync setup.

{% include footer.html %}