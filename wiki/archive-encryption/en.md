# Archive encryption
**This feature is available from version: _3.3_**

If you want to encrypt the configuration archive, whether for data protection reasons or something else, you can use the archive encryption feature in the SaveDesktop app. So, how does it work, and how to set it up?

## How does it work?
If this feature is enabled, SaveDesktop will always ask you to create a password for your new archive of the configuration. The criteria for the password include at least 12 characters, one uppercase letter, one lowercase letter, and one special character. If the password doesn't meet these criteria, it will not be possible to continue saving configuration. 

The archive will be saved as a ZIP archive (because Tar doesn't support the password protection feature), and if you want to extract it, you will be asked to enter the password that you used in the saving configuration process. The same applies in the case of configuration import.

If you forgot the password, it will not possible to extract the archive and use it in the importing configuration process.

> [!WARNING]  
> The periodic saving files are (so far) not available to protect with a password. Encrypted archives are, so far, not possible to use in synchronization.

## How to set it up?
In the 3.3 version, the interface has been slightly modified, specifically, periodic saving section is now located under the "More options" button. On the same place, is located archive encryption section. So click on the already mentioned button, and enable Archive encryption switch.

_If you have any questions, you can use Github issues._

{% include footer.html %}
