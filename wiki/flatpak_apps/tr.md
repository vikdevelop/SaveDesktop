# Kaydetme, içe aktarma, ve Flatpak uygulamarını senkronize et

Save Desktop; Flatpak uygulamalarını kullanıcı verileriyle birlikte, ayrıca simgeler, temalar, ayarlar ve eklentilerle beraber
kaydetmenize, içe aktarmanıza ve senkronize etmenize olanak tanır.

## Where can I find this?

Flatpak-related options are located in the **Select configuration items** dialog.
You can open it from the header menu (three dots in the window title bar).

## Available options

### List of installed Flatpak apps

Saves and restores the list of installed Flatpak applications.

### User data of installed Flatpak apps

Allows you to include user data of selected Flatpak applications.
Click the **">"** button to choose which apps should have their data saved.

### Keep installed Flatpak apps and data (enabled by default)

When enabled, Save Desktop **will NOT remove Flatpak applications or their data that are not present in the archive**.

When disabled, Save Desktop will **remove any installed Flatpak apps that are not listed in the imported archive — including their user data**.

⚠️ **Warning:**
Disable this option only if you intentionally want your system to exactly match the imported archive. Removed applications and their data **cannot be recovered**.

## How does importing work?

After selecting an archive or folder, you will be asked which configuration items should be imported.
Click **Apply** to start the import process.

Import order:

1. Desktop configuration (icons, themes, fonts, extensions, settings, etc.)
2. Flatpak applications and their user data (after next login)

Flatpak installation and removal start **after you log back into the system**.

### Synchronization mode

In synchronization mode, Flatpak applications are processed **immediately after synchronization finishes** (no relog required).

## Önemli not

Eğer **Flatpak uygulamalarını ve verilerini koru** seçeneği devre dışıysa
ve içe aktarılan arşivde yer almayan Flatpak uygulamaları yüklüyse,
**bu uygulamalar kullanıcı verileriyle birlikte kalıcı olarak silinir.**

{% include footer.html %}