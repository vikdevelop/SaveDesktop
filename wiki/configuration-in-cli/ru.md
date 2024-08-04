## Saving configuration

**This feature is available from version: `3.3`**

If you prefer command-line interface (CLI) before graphical user interface (GUI), SaveDesktop in addition to saving configuration in the GUI, allows you save configuration in the CLI.

### So how to proceed?

**1. Open a terminal**

You can open it from the applications menu, or by using the Ctrl+Alt+T keyboard shortcut.

**2. Enter the command**

Enter the following command in the terminal:
- if you have SaveDesktop installed as a Flatpak package, use the following:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --save-now
     ```

- if you have SaveDesktop installed as a Snap or native package, use:
     ```
     savedesktop --save-now
     ```

When using this method, it uses parameters from the GUI, specifically parameters from the periodic saving mode, such as filename format and selected folder for periodic saving files. You can save the configuration with this method whenever you want, regardless of the selected periodic saving interval.

## Importing configuration

**Эта функция доступна начиная с версии: `3.2.2`**

Помимо импорта конфигурации в графическом интерфейсе, SaveDesktop также позволяет импортировать конфигурацию в интерфейсе командной строки (CLI), который вы можете использовать в случае сбоя вашей среды рабочего стола.

### Итак, как действовать?
**1. Откройте терминал**

Открыть его можно из меню приложений или с помощью комбинации клавиш Ctrl+Alt+T.

**2. Enter the command**

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

_Если у вас есть вопросы, вы можете использовать задачи GitHub._

{% include footer.html %}
