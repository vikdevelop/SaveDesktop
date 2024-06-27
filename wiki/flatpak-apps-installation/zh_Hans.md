# 保存已安装的Flatpak应用并通过列表进行安装
自2.5版本以后，SaveDesktop允许您保存已安装的Flatpak应用，并支持通过列表安装Flatpak应用。那么它是如何工作的呢？

### 保存已安装的Flatpak应用
为已安装的Flatpak应用建立列表是可行的。列表将读取系统安装路径/var/lib/flatpak/app和用户安装路径~/.local/share/flatpak/app中的应用，而保存好的列表将位于存档文件中的installed_flatpaks.sh和installed_user_flatpaks.sh，它们同样分别对应系统安装和用户安装。

### 从列表安装Flatpak应用
当完成导入并重新登录后，**Flatpak应用将在后台自动安装。**

_如果您遇到任何问题，可使用GitHub提交issues。_
