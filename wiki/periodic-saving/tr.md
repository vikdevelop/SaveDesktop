# Periyodik kaydetme
Manuel kaydetmeye ek olarak SaveDesktop, masaüstü yapılandırmanızı düzenli aralıklarla kaydetmenize de olanak tanır. Aşağıdaki seçenekler arasından seçim yapabilirsiniz:
- **Günlük**:
  - Sisteme giriş yapıldıktan sonra SaveDesktop arka planda çalışır ve yedeklemeyi yapar. Gün içinde tekrar giriş yapıldığında yeni yedek almaz, günlük yedek bir kere yapılır.
- **Haftalık**:
  - SaveDesktop, "Haftalık" ayarlanırsa, her pazartesi yedekleme yapar. Yedekleme günü giriş yapılmazsa ertesi gün yedekleme yapılmaz.
- **Aylık**:
  - SaveDesktop, "Aylık" ayarlanırsa, yedeklemeyi ayın ilk gününde yapar, örn. 1 Mayıs, 1 Haziran, 1 Aralık vb. "Haftalık"ta olduğu gibi yedekleme günü giriş yapılmazsa SaveDesktop ertesi gün yedekleme yapmaz.
- **Asla**:
  - Hiçbir şey yapmaz

### Periyodik kayıtta dosyalar nerede saklanıyor?
Periyodik kayıtta varsayılan kaydetme dizini `/home/user/Downloads/SaveDesktop/archives`tır, ancak özel bir dizin seçilebilir.

### Dosya adı formatı
If you want to give a filename format for periodic saving files other than `Latest_configuration`, it is possible, even with spaces. Since version 2.9.6, variable `{}` doesn't work for setting the today date because now, in every periodic saving, the original backup file is overwritten.



{% include footer.html %}
