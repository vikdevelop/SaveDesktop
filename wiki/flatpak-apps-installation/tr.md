{% include head.html %}

# Save installed Flatpak apps and install them from list
Since version 2.5, SaveDesktop allows you to save installed Flatpak applications and install them from a list. So how does it work?

### Saving installed Flatpak applications
It is possible to save a list of installed Flatpak applications installed in the system directory /var/lib/flatpak/app and the home directory ~/.local/share/flatpak/app. The list of installed Flatpak applications in the configuration archive is marked as installed_flatpaks.sh for the system directory and installed_user_flatpaks.sh for the home directory.

### Installing Flatpak applications from the list
After importing the saved configuration file and logging back in, **the Flatpak applications will start installing in the background.**



{% include footer.html %}
