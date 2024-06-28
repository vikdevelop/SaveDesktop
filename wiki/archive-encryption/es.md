# Cifrado de archivos
**Esta función está disponible a partir de la versión: 3.3**

Si quieres cifrar el archivo de configuración, ya sea por motivos de protección de datos o por cualquier otro motivo, puedes utilizar la función de cifrado de archivos de la aplicación SaveDesktop. Entonces, ¿cómo funciona y cómo se configura?

## ¿Cómo funciona?
Si esta función está activada, SaveDesktop siempre le pedirá que cree una contraseña para su nuevo archivo de la configuración. Los criterios para la contraseña incluyen al menos 8 caracteres, una letra mayúscula, una letra minúscula y un carácter especial. Si la contraseña no cumple estos criterios, no será posible continuar guardando la configuración.

El archivo se guardará como un archivo ZIP (porque Tar no soporta la función de protección por contraseña), y si desea extraerlo, se le pedirá que introduzca la contraseña que utilizó en el proceso de guardar la configuración. Lo mismo ocurre en el caso de la importación de la configuración.

Si olvida la contraseña, no será posible extraer el archivo y utilizarlo en el proceso de importación de la configuración.

> [!WARNING]  
> The periodic saving files are (so far) not available to protect with a password. Encrypted archives are, so far, not possible to use in synchronization.

## ¿Cómo configurarlo?
En la versión 3.3, la interfaz ha sido ligeramente modificada, en concreto, la sección de guardado periódico se encuentra ahora bajo el botón "Más opciones". En el mismo lugar, se encuentra la sección de encriptación de archivos. Así que haz click en el botón ya mencionado, y activa el interruptor de encriptación de archivos.

_Si tiene alguna duda, utilice el notificador de incidencias de GitHub._
