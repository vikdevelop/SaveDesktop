
## Сохранение конфигурации

**Эта функция доступна начиная с версии: `3.3`**

Если вы предпочитаете интерфейс командной строки (CLI) графическому интерфейсу пользователя (GUI), SaveDesktop в дополнение к сохранению конфигурации в GUI позволяет вам сохранять конфигурацию в CLI.

### Итак, как действовать?
**1. Откройте терминал**

Открыть его можно из меню приложений или с помощью комбинации клавиш Ctrl+Alt+T.

**2. Введите команду для импорта конфигурации**

Введите следующую команду в терминале:
- если SaveDesktop у вас установлен как пакет Flatpak, используйте следующее:
     ```
     flatpak run io.github.vikdevelop.SaveDesktop --save-now
     ```
- если SaveDesktop у вас установлен как Snap или нативный пакет, используйте: 
     ```
     savedesktop --save-now
     ```

При использовании этого метода он использует параметры из графического интерфейса пользователя, в частности параметры из режима периодического сохранения, такие как формат имени файла и выбранная папка для периодического сохранения файлов. Вы можете сохранить конфигурацию с помощью этого метода в любое удобное для вас время, независимо от выбранного интервала периодического сохранения.

## Импорт конфигурации

**Эта функция доступна начиная с версии: `3.2.2`**

Помимо импорта конфигурации в графическом интерфейсе, SaveDesktop также позволяет импортировать конфигурацию в интерфейсе командной строки (CLI), который вы можете использовать в случае сбоя вашей среды рабочего стола.

### Итак, как действовать?
**1. Откройте терминал**

Открыть его можно из меню приложений или с помощью комбинации клавиш Ctrl+Alt+T.

**2. Введите команду для импорта конфигурации**

Введите следующую команду в терминале:
- если SaveDesktop у вас установлен как пакет Flatpak, используйте следующее:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --import-config /path/to/filename.sd.tar.gz
     ```

- если SaveDesktop у вас установлен как Snap или нативный пакет, используйте: 
     ```
     savedesktop --import-config /path/to/filename.sd.tar.gz
     ```

**Примечание**:
- вместо `/path/to/filename.sd.tar.gz` введите путь к архиву конфигурации, который вы хотите импортировать, например: `/home/user/Downloads/myconfig.sd.tar.gz`



{% include footer.html %}