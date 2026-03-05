# Menyimpan, mengimpor, dan menyinkronkan aplikasi Flatpak

Save Desktop memungkinkan Anda menyimpan, mengimpor, dan menyinkronkan aplikasi Flatpak beserta data penggunanya, selain ikon, tema, pengaturan, dan ekstensi.

## Di mana saya dapat menemukannya?

Opsi terkait Flatpak terletak di dialog **Pilih item konfigurasi**.
Anda dapat membukanya dari menu header (tiga titik di bilah judul jendela).

## Opsi yang tersedia

### Daftar aplikasi Flatpak yang terinstal

Menyimpan dan memulihkan daftar aplikasi Flatpak yang terinstal.

### Data pengguna aplikasi Flatpak yang terinstal

Memungkinkan Anda menyertakan data pengguna dari aplikasi Flatpak yang dipilih.
Klik tombol **">"** untuk memilih aplikasi mana yang datanya harus disimpan.

### Pertahankan aplikasi dan data Flatpak yang terinstal (diaktifkan secara default)

Saat diaktifkan, Save Desktop **TIDAK akan menghapus aplikasi Flatpak atau datanya yang tidak ada dalam arsip**.

Saat dinonaktifkan, Save Desktop akan **menghapus aplikasi Flatpak yang terinstal yang tidak tercantum dalam arsip yang diimpor — termasuk data penggunanya**.

⚠️ **Peringatan:**
Nonaktifkan opsi ini hanya jika Anda sengaja ingin sistem Anda persis sesuai dengan arsip yang diimpor. Aplikasi yang dihapus beserta datanya **tidak dapat dipulihkan**.

## Bagaimana cara impor bekerja?

Setelah memilih arsip atau folder, Anda akan ditanya item konfigurasi mana yang harus diimpor.
Klik **Terapkan** untuk memulai proses impor.

Urutan impor:

1. Konfigurasi desktop (ikon, tema, font, ekstensi, pengaturan, dll.)
2. Aplikasi Flatpak dan data penggunanya (setelah login berikutnya)

Instalasi dan penghapusan Flatpak dimulai **setelah Anda masuk kembali ke sistem**.

### Mode sinkronisasi

Dalam mode sinkronisasi, aplikasi Flatpak diproses **segera setelah sinkronisasi selesai** (tidak perlu masuk ulang).

## Catatan penting

Jika **Pertahankan aplikasi dan data Flatpak yang terinstal** dinonaktifkan dan Anda memiliki aplikasi Flatpak yang terinstal yang tidak termasuk dalam arsip yang diimpor, aplikasi tersebut akan **dihapus secara permanen beserta data penggunanya**.

{% include footer.html %}