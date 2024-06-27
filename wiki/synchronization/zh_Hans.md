# 通过网络在不同计算机中同步
## 如何设置？
### 您有什么需求？
**在计算机1上:**
- 手动设置您想同步的设备的IP地址，以便每次启动时，IP地址不会发生变化。您可通过以下方式进行设置：

  **路由器设置**
  - [Asus路由器](https://www.asus.com/support/FAQ/1000906/)
  - [Tp-link路由器](https://www.tp-link.com/us/support/faq/170/)
  - [Tenda路由器](https://www.tendacn.com/faq/3264.html)
  - [Netgear路由器](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - 如果您没有以上路由器，请打开您的路由器设置界面(URL: [192.168.1.1](http://192.168.1.1)或类似地址)然后搜索DHCP服务器部分，看是否有类似“手动设置IP地址至DHCP列表”或“静态IP”等。

  **关于`system-config-printer`包:**  <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
  
  - 如果您不想从路由器界面手动设置IP地址，并且您有连接打印机，且安装过`system-config-printer`包，请检查是否勾选了“共享”选项，您可从标题栏点击打印机选项卡以查看。如果您没有勾选，请勾选上它，并重启系统。[这里](https://github-production-user-asset-6210df.s3.amazonaws.com/83600218/272054218-ff17c19b-98f5-41fe-8f34-40de275f0da4.png) 有一张实例截图.

**在计算机2上:**
- 请检查此设备是否已与计算机1同处一个局域网内。

### 在SaveDesktop应用中设置同步
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

在计算机1和2上同时打开SaveDesktop应用，并切换至同步页面。在计算机1上点击“配置同步文件，并选择同步文件（您的定期存档文件），并选择一个定期同步间隔。接着复制同步URL，到计算机2上，点击“连接至其他计算机”并填入从计算机1上复制好的URL。

如果您想从计算机2同步桌面环境配置至计算机1，也是相同的步骤。

**您需要注销以生效**

## 定期同步
您可从以下方案中选择:
- 每日
- 每周（在每个周二会进行同步）
- 每月（在每月第二天会进行同步）
- 手动（可手动点击标题栏的三点按钮进行手动同步）
- 从不（无事发生）

_如果您遇到任何问题，可使用GitHub提交issues。_


