# Contributing to the SaveDesktop app
First, thanks for your interest in the contribution to this app, I appreciate it!

There are a couple of ways to contribute to this app:

## Translations
Thanks to the community, SaveDesktop is translated into more than 20 languages. However, if your language is not available in the app or if your language in the app is not complete, feel free to add or edit it using [Weblate](https://hosted.weblate.org/projects/vikdevelop/savedesktop/)!

It is also possible to translate the application wiki using the same tool [here](https://hosted.weblate.org/projects/vikdevelop/savedesktop-github-wiki).

To add or modify an existing language, you must be registered for Weblate, which can be done via email, a Github or Google account, and many other services.

## Involvement in development
The SaveDesktop application is written in Python 3 using [GTK 4.0](https://docs.gtk.org/gtk4/) and [LibAdwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/index.html) libraries, so if you have knowledge of Python and, ideally, in combination with these libraries, your contributions are welcome!
If you don't know how to contribute specifically, you can check out the [issues marked as “good first issue”](https://github.com/vikdevelop/SaveDesktop/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

No Python knowledge? Never mind. For example, you can contribute to the [application wiki](https://github.com/vikdevelop/SaveDesktop/tree/webpage/wiki) (improve webpage style, add screenshots in the `wiki/synchronization/screenshots` directory, etc.)

### So how to proceed?
1. Fork this repository *(see the [Github docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) for more information)*
2. Go to your fork of this repository *(e.g., https://github.com/<your_username>/SaveDesktop)*
3. Make changes you want
4. If you want to test your changes, you can proceed as follows:
    - clone your fork
      ```bash
      git clone https://github.com/<your_username>/SaveDesktop
      ```
    - go to the cloned fork folder
      ```bash
      cd SaveDesktop
      ```
    - build the application using Flatpak Builder
      - if you have not installed org.gnome.Sdk (the latest version) runtime, install it using this command: `flatpak install runtime/org.gnome.Sdk/x86_64/[GNOME's latest version] -y`
      ```bash
      flatpak-builder build *.yaml --install --user
      ```
      - alternatively, you can build a native version as follows (assuming you have GTK 4.0 and LibAdwaita libraries in the latest version):
        ```bash
        sh native/directories.sh --install
        ```
5. Once you are happy with your changes, submit a pull request to this repository, which I will review and merge with my repository if necessary.

*It should be noted that this app is available under the [GNU GPL 3.0](https://github.com/vikdevelop/SaveDesktop/blob/main/LICENSE) license, so it is necessary to follow the license conditions.*

## Reporting issues
Have you found a bug in the app? Do you have a suggestion for a new feature, or is something not clear? You can use [Github issues](https://github.com/vikdevelop/SaveDesktop/issues) for this purpose, but make sure someone else hasn't reported a similar issue before you. Don't prefer Github issues? If so, you can use [this form](https://vikdevelop.github.io/SaveDesktop/open-issue/) or [Github discussions](https://github.com/vikdevelop/SaveDesktop/discussions).

**I look forward to your contributions to this app!**
