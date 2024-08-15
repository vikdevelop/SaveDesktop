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

**自`3.2.2`版本起，该功能已实现。**

除了通过图形界面导入配置，SaveDesktop也允许您通过命令行界面（CLI）导入配置，当您的桌面环境受损时，这也许会很有用。

### 那么该如何实现呢?
**1. 打开一个终端**

您可通过应用菜单，或者通过快捷键比如Ctrl+Alt+T来打开。

**2. Enter the command**

在终端里输入以下命令:
- 如果您通过Flatpak安装了SaveDesktop，则输入：

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --import-config /path/to/filename.sd.tar.gz
     ```

- 如果您通过Snap或本地包安装，则输入：
     ```
     savedesktop --import-config /path/to/filename.sd.tar.gz
     ```

**请注意**:
- 应当输入您想导入的配置文件的实际路径以取代`/path/to/filename.sd.tar.gz`，比如：`/home/user/Downloads/myconfig.sd.tar.gz`



{% include footer.html %}
