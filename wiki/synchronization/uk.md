# Синхронізація між комп'ютерами в мережі
## Як його налаштувати?
### Що вам потрібно?
**На комп'ютері 1:**
- вручну призначте IP-адреси ваших пристроїв, які ви хочете синхронізувати, щоб IP-адреса не змінювалася при кожному включенні комп'ютера. Це можливо налаштувати через:

  **Router settings:**
  - [для роутерів Asus](https://www.asus.com/support/FAQ/1000906/)
  - [для роутерів Tp-link](https://www.tp-link.com/us/support/faq/170/)
  - [для роутерів Tenda](https://www.tendacn.com/faq/3264.html)
  - [для роутерів Netgear](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - якщо у вас немає перерахованих вище роутерів, відкрийте налаштування роутера (URL: [192.168.1.1](http://192.168.1.1) або пов'язані з ними) і шукайте в розділі DHCP сервера щось у формі «Вручну призначити IP списку DHCP» або «Статичний IP» і т.д.
  
  **`system-config-printer` package:** <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
  - if you don't want to set the IP address manually from the router interface, and if you have a printer and installed `system-config-printer` package, check if you ticked the option "Shared" by clicking Printer tab on the header bar. If not, please tick it and reboot the system. [Here](https://github-production-user-asset-6210df.s3.amazonaws.com/83600218/272054218-ff17c19b-98f5-41fe-8f34-40de275f0da4.png) is a screenshot, what it's supposed to look like.

**На комп'ютері 2:**
- Перевірте, чи під'єднані ви тієї мережі, що і комп'ютер 1.

### Встановити синхронізацію в додатку SaveDesktop
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

На комп'ютерах 1 і 2 відкрийте додаток SaveDesktop і перейдіть на сторінку «Синхронізувати». На комп'ютері 1 натисніть кнопку «Налаштувати файл синхронізації», виберіть файл синхронізації і виберіть періодичний інтервал синхронізації. Потім скопіюйте URL для синхронізації і на комп'ютері 1, натисніть на кнопку «З'єднатися з іншим комп'ютером» і введіть скопійований URL для синхронізації з комп'ютера 1.

Якщо ви хочете синхронізувати конфігурацію середовища стільниці з комп'ютера 2 з комп'ютером 1, виконайте ту ж процедуру.

**Щоб зміни набули чинності, необхідно вийти з системи**

## Періодична синхронізація
Ви можете вибрати один з наступних пунктів:
- Щодня
- Щотижня (синхронізація відбувається щовівторка)
- Щомісяця (синхронізація відбувається кожен другий день місяця)
- Вручну (можна синхронізувати конфігурацію з меню в рядку заголовка, натиснувши на три точки)
- Ніколи (нічого не буде відбуватися)

_Якщо у вас є якісь запитання, відкрийте новий `Issues` у GitHub репозиторії._
