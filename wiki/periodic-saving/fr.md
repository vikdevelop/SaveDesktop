# Sauvegardes régulière
### Comment ça marche ?
En plus des sauvegardes manuelles, SaveDesktop vous permets aussi de sauvegarder la configuration de votre bureau de façon périodique. Vous pouvez choisir parmi les options suivantes:
- **Daily**: 
  - After logging into the system, SaveDesktop starts in the background and backs up the configuration. If you then log back in this day, it will not do it again, because it has already been created for that day.
- **Weekly**:
  - SaveDesktop performs a configuration backup every Monday if "Weekly" is selected. If the computer is not running on that day, SaveDesktop does not do it the next day.
- **Monthly**:
  - If "Monthly" is selected, SaveDesktop makes the backup on the first day of the month, e.g. May 1, June 1, December 1, etc. As with "Weekly", if the computer is not running on that day, SaveDesktop does not perform it the next day.
- **Never**:
  - Nothing's happening

### Where are the periodic saving files stored?
Default directory for periodic saving is `/home/user/Downloads/SaveDesktop/archives`, but you can choose custom directory.

### Filename format
If you want to give a filename format for periodic saving files other than `Latest_configuration`, it is possible, even with spaces. Since version 2.9.6, variable `{}` doesn't work for setting the today date because now, in every periodic saving, the original backup file is overwritten.

_If you have any questions, you can use Github issues._
