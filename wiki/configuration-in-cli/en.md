## Saving configuration

**This feature is available from version: `3.3`**

If you prefer command-line interface (CLI) before graphical user interface (GUI), SaveDesktop in addition to saving configuration in the GUI, allows you save configuration in the CLI.

### So how to proceed?

**1. Open a terminal**

You can open it from the applications menu, or by using the Ctrl+Alt+T keyboard shortcut.

**2. Type the command to import the configuration**

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
**This feature is available from version: `3.2.2`**

In addition to importing configuration in the GUI, SaveDesktop also allows you to import configuration in the command line interface (CLI), which you can use in case your desktop environment breaks.

### So how to proceed?
**1. Open a terminal**

You can open it from the applications menu, or by using the Ctrl+Alt+T keyboard shortcut.

**2. Type the command to import the configuration**

Enter the following command in the terminal:
- if you have SaveDesktop installed as a Flatpak package, use the following:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --import-config /path/to/filename.sd.tar.gz
     ```

- if you have SaveDesktop installed as a Snap or native package, use: 
     ```
     savedesktop --import-config /path/to/filename.sd.tar.gz
     ```

> [!NOTE]
> instead of `/path/to/filename.sd.tar.gz`, enter the path to the configuration archive you want to import, for example: `/home/user/Downloads/myconfig.sd.tar.gz`

_If you have any questions, you can use Github issues._
