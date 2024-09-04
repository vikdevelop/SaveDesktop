# Sincronización entre ordenadores de la red
#### Requisitos
- Debes tener una carpeta creada que se sincronice con tu almacenamiento en la nube en cada ordenador que quieras sincronizar. Esto se puede hacer usando:

  <details>
      <summary>
        <b>Cuentas en línea de GNOME</b>
        <p>(para entornos de escritorio GNOME, Cinnamon, COSMIC (antiguo) y Budgie)</p>
      </summary>

    - Abrir la configuración de GNOME
    - Vaya a la sección Cuentas en línea y seleccione su servicio de unidad en la nube

      ![OnlineAccounts.png](https://raw.githubusercontent.com/vikdevelop/SaveDesktop/webpage/wiki/synchronization/screenshots/OnlineAccounts_en.png)
    
  </details>

  <details>
      <summary>
        <b>Rclone</b>
        <p>(para otros entornos de escritorio)</p>
      </summary>

    - Instalar Rclone
      ```
      sudo -v ; curl https://rclone.org/install.sh | sudo bash
      ```
      
    - Configurar Rclone usando este comando, que crea la carpeta de la unidad de la nube, configura Rclone y monta la carpeta
      ```
      mkdir -p ~/drive && rclone config create drive your-cloud-drive-service && nohup rclone mount drive: ~/drive --vfs-cache-mode escribe & echo "La unidad ha sido montada correctamente"
      ```
      * En lugar de `your-cloud-drive-service` use el nombre de su servicio de disco en la nube, como `drive` (para Google Drive), `onedrive`, `dropbox`, etc.

    - Permitir el acceso a la carpeta creada en la [aplicación Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal).
  </details>
  
## Configurar la sincronización en la aplicación SaveDesktop
En la primera computadora:
1. Abra la aplicación SaveDesktop
2. En la página Sync, haga clic en el botón "Configurar el archivo de sincronización" y luego en el botón "Cambiar"
3. Haga clic en "Guardar periódicamente" y seleccione la carpeta que se sincroniza con su almacenamiento en la nube como una carpeta de ahorro periódico
4. Si el archivo de guardado periódico no existe, haga clic en el botón Crear

En el segundo ordenador:
1. Abra la aplicación SaveDesktop
2. Vaya a la página Sincronizar y haga clic en el botón "Conectar con el almacenamiento en la nube".
3. Haz clic en el botón "Seleccionar carpeta de unidad en la nube" y selecciona la carpeta que está sincronizada con el mismo almacenamiento en la nube que el primer ordenador.
4. Selecciona el intervalo de sincronización periódica, ya que si lo dejas en Nunca, la sincronización no funcionará.

Para configurar la sincronización bidireccional, asegúrate de tener seleccionada la misma carpeta en la nube en el cuadro de diálogo "Conectar con el almacenamiento en la nube" en el primer ordenador, el intervalo de sincronización periódica seleccionado y el interruptor de "Sincronización bidireccional" activado.

### Sincronización periódica
Puede elegir entre las siguientes opciones:
- Diariamente
- Semanal (la sincronización tiene lugar cada martes)
- Mensualmente (la sincronización tiene lugar cada dos días del mes)
- Manualmente (es posible sincronizar la configuración desde el menú de la barra de cabecera haciendo clic en los tres puntos)
- Nunca (no ocurre nada)

{% include footer.html %}
