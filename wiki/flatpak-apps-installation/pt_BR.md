
# Salve os aplicativos Flatpak instalados e instale-os a partir de uma lista
Desde a versão 2.5, o SaveDesktop permite que você salve os aplicativos Flatpak instalados e instale-os a partir de uma lista. Então, como isso funciona?

### Salvar aplicativos Flatpak instalados
É possível salvar uma lista dos aplicativos Flatpak instalados no diretório de sistema /var/lib/flatpak/app e no diretório pessoal ~/.local/share/flatpak/app. A lista de aplicativos Flatpak instalados presente no arquivo de configuração fica marcada como installed_flatpaks.sh para os apps do diretório de sistema e como installed_user_flatpaks.sh para os do diretório pessoal.

### Instalar aplicativos Flatpak a partir da lista
Após importar o arquivo de configuração salvo e logar de volta no sistema, **os aplicativos Flatpak começarão a ser instalados em segundo plano.**



{% include footer.html %}
