# Sincronización entre ordenadores de la red
## ¿Cómo se configura?
### ¿Qué necesitas?
**En el ordenador 1:**
- asigna manualmente las direcciones IP de los dispositivos que quieras sincronizar para que la dirección IP no cambie cada vez que se encienda el ordenador. Es posible configurarlo a través de:

  **Configuración del router:**
  - [para routers Asus](https://www.asus.com/support/FAQ/1000906/)
  - [para routers Tp-link](https://www.tp-link.com/us/support/faq/170/)
  - [para routers Tenda](https://www.tendacn.com/faq/3264.html)
  - [para routers Netgear](https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router)
  - si no tienes los routers mencionados, abre la configuración de tu router (URL: [192.168.1.1](http://192.168.1.1) o relacionadas) y busca en la sección del servidor DHCP algo en forma de "Asignar manualmente una IP a la lista DHCP" o "IP estática", etc.

  **Paquete `system-config-printer`:** <img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/ff4e742d-07e2-453f-8ace-b51b4f52d1dd" width="85">
  - Si no desea asignar una IP manual al router y tiene una impresora instalada en su sistema, además del paquete `system-config-printer`, verifique que la opción "Compartida" está activada en el panel principal de la impresora. De lo contrario, active esta opción y reinicie el sistema. [Aquí](https://raw.githubusercontent.com/BennyBeat/SaveDesktop/1602010b7ef88f3fb0eb1010af33571f0c548eb3/translations/wiki/es-Printer.png) tiene una captura de pantalla con la configuración idónea.

**En el ordenador 2:**
- Compruebe si está conectado a la misma red que el ordenador 1.

### Configuración de la sincronización en la aplicación SaveDesktop
<a href="https://www.youtube.com/watch?v=QccFR06oyXk"><img src="https://github.com/vikdevelop/SaveDesktop/assets/83600218/a4f8da24-7183-49e1-9a58-82092a42f124" height="32"></a>

En los ordenadores 1 y 2, abra la aplicación SaveDesktop y vaya a la página Sincronización. En el ordenador 1, haga clic en el botón "Configurar el archivo de sincronización", seleccione el archivo de sincronización (su archivo de guardado periódico) y seleccione un intervalo de sincronización periódica. A continuación, copie la URL para la sincronización y, en el ordenador 2, haga clic en el botón "Conectar con otro ordenador" e introduzca la URL copiada para la sincronización desde el ordenador 1.

Si desea sincronizar el entorno de escritorio del ordenador 2 al 1, los pasos son los mismos.

**Es necesario cerrar y volver a abrir la sesión para aplicar los cambios**

## Sincronización periódica
Puede elegir entre los siguientes elementos:
- Diariamente
- Semanalmente (la sincronización se lleva a cabo cada martes)
- Mensualmente (la sincronización se lleva a cabo el segundo día de cada mes)
- Manualmente (es posible realizar la sincronización en cualquier momento desde el menú principal al hacer clic en los tres puntos)
- Nunca (no se realiza ningún cambio)



{% include footer.html %}
