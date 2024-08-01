# Synchronization between computers in the network
## How to set it up?
### What's your needing?
**On computer 1:**
- manually assign the IP addresses of your devices that you want to sync so that the IP address does not change every time the computer is turned on. It is possible to set it via:

  **Router settings:**
  - [for Asus routers](https://www.asus.com/support/FAQ/1000906/)
  - [for Tp-link routers](https://www.tp-link.com/us/support/faq/170/)
  - [for Tenda routers](https://www.tendacn.com/faq/3264.html)
  - [for Netgear routers](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - if you don't have the above routers, open your router settings (URL: [192.168.1.1](http://192.168.1.1) or related) and search in the DHCP server section something in the shape of "Manually assign an IP to the DHCP list" or "Static IP", etc.

  **`system-config-printer` package:**  <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">

  - if you don't want to set the IP address manually from the router interface, and if you have a printer and have installed `system-config-printer` package, check if you ticked the option "Shared" by clicking the Printer tab on the header bar. If not, please tick it and reboot the system. [Here](https://github-production-user-asset-6210df.s3.amazonaws.com/83600218/272054218-ff17c19b-98f5-41fe-8f34-40de275f0da4.png) is a screenshot, what it's supposed to look like.

**On computer 2:**
- Check if you are connected to the same network as computer 1.

### Set synchronization in the SaveDesktop app
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

On computer 1 and 2, open the SaveDesktop application and switch to the Sync page. On computer 1, click on the button "Set up the sync file", select the synchronization file (your periodic saving file), and select a periodic synchronization interval. Then copy the URL for synchronization, and on computer 2, click on the button "Connect with other computer" and enter the copied URL for synchronization from computer 1.

If you want to sync the DE configuration from computer 2 to computer 1, follow the same procedure.

**For the changes to take effect, it is necessary to logout from system**

## Periodic synchronization
You can choose between the following items:
- Daily
- Weekly (synchronization takes place every Tuesday)
- Monthly (synchronization takes place every second day in the month)
- Manually (it is possible to sync configuration from the menu in the header bar by clicking on the three dots)
- Never (nothing's happening)

_If you have any questions, you can use GitHub issues._

{% include footer.html %}
