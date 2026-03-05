# Sinkronisasi antar komputer dalam jaringan

Selain menyimpan konfigurasi dan mengimpornya, Save Desktop juga memungkinkan Anda menyinkronkannya antar komputer di jaringan menggunakan folder cloud bersama atau folder Syncthing bersama.

## Pengaturan di Komputer Pertama
1. Buka halaman **Sinkronisasi** di aplikasi Save Desktop.
2. Klik **"Siapkan berkas sinkronisasi."**
3. Wizard pengaturan cepat akan muncul:
   * Jika Anda menggunakan GNOME, Cinnamon, Budgie, atau COSMIC versi lama, metode **Akun Online GNOME** digunakan.
   * Untuk KDE Plasma atau desktop lainnya, beralih ke **Rclone** (Anda hanya perlu menyalin perintah dan menempelkannya ke terminal).
   * Sebagai alternatif, Anda dapat menggunakan **Syncthing** dengan mengklik **"Gunakan folder Syncthing sebagai gantinya"** dan memilih folder yang disinkronkan.
4. Setelah menyelesaikan wizard, dialog **"Siapkan berkas sinkronisasi"** akan terbuka:
   * Sebuah **berkas penyimpanan berkala** (arsip konfigurasi desktop Anda) akan mulai dibuat di dalam folder yang dipilih.
   * Anda dapat mengubah interval atau nama berkas menggunakan tombol **"Ubah"**.
5. Klik **"Terapkan"**:
   * Berkas kedua, `SaveDesktop.json`, dibuat di folder yang sama. Berkas ini berisi nama berkas sinkronisasi dan interval penyimpanan.
   * Anda akan diminta untuk **keluar** dari sesi agar sinkronisasi dapat sepenuhnya aktif.

## Menghubungkan di Komputer Lain
1. Di komputer lain, buka halaman **Sinkronisasi** lagi.
2. Klik **"Hubungkan ke penyimpanan cloud."**
3. Wizard yang sama akan muncul – pilih folder yang disinkronkan melalui GNOME OA, Rclone, atau Syncthing.
4. Setelah wizard:
   * Dialog **"Hubungkan ke penyimpanan cloud"** terbuka.
 * Pilih **interval sinkronisasi** dan aktifkan atau nonaktifkan **Sinkronisasi dua arah**.
5. Klik **"Terapkan"**:
   * Anda akan diminta untuk **keluar**, atau (jika menggunakan sinkronisasi manual) diberitahu bahwa Anda dapat menyinkronkan dari menu header aplikasi.
 * Setelah masuk kembali, Save Desktop terhubung ke folder bersama dan menyinkronkan konfigurasi Anda secara otomatis, dengan notifikasi di awal dan akhir.

### Sinkronisasi Dua Arah
Jika **Sinkronisasi dua arah** diaktifkan di kedua komputer:
* Save Desktop menyalin pengaturan sinkronisasi (seperti interval dan nama berkas) dari satu mesin ke mesin lainnya,
* Ini menjaga sistem Anda tetap tersinkronisasi tanpa perlu mengonfigurasi masing-masing secara manual.

## Berkas yang Digunakan dalam Sinkronisasi
* **Berkas penyimpanan berkala** – arsip `.sd.zip` dari konfigurasi desktop Anda, diperbarui secara berkala.
* **SaveDesktop.json** – berkas pembantu kecil yang menyimpan nama berkas arsip dan interval penyimpanan, digunakan selama pengaturan sinkronisasi.

{% include footer.html %}