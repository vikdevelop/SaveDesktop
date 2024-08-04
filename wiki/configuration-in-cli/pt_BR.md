# Salvar configuração
**Essa funcionalidade está disponível a partir da versão: `3.3`**

Se você preferir a interface de linha de comando (CLI) à interface gráfica de usuário (GUI), o SaveDesktop, além de salvar sua configuração pela GUI, também te permite salvar sua configuração pela CLI.

### Então, como proceder?
**1. Abra um terminal**

Você pode abri-lo pelo menu de aplicativos, ou usando o atalho de teclado Ctrl+Alt+T.

**2. Enter the command**

Insira o seguinte comando no terminal:
- se você tiver o SaveDesktop instalado como um pacote Flatpak, use o seguinte comando:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --save-now
     ```

- se você tiver o SaveDesktop instalado como um pacote Snap ou um pacote nativo, use: 
     ```
     savedesktop --save-now
     ```

Ao usar este método, ele usa parâmetros da GUI, especificamente parâmetros do modo de salvamento periódico, como o formato de nome de arquivo e a pasta selecionada para os arquivos de salvamento periódico. Você pode salvar a configuração com esse método quando quiser, independente do intervalo de salvamento periódico escolhido.

# Importar configuração
**Essa funcionalidade está disponível a partir da versão: `3.2.2`**

Além de importar configurações pela GUI, o SaveDesktop também permite que você importe configurações pela interface de linha de comando (CLI), a qual você pode usar caso o seu ambiente de área de trabalho quebre.

### Então, como proceder?
**1. Abra um terminal**

Você pode abri-lo pelo menu de aplicativos, ou usando o atalho de teclado Ctrl+Alt+T.

**2. Enter the command**

Insira o seguinte comando no terminal:
- se você tiver o SaveDesktop instalado como um pacote Flatpak, use o seguinte comando:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --import-config /caminho/para/nomedoarquivo.sd.tar.gz
     ```

- se você tiver o SaveDesktop instalado como um pacote Snap ou um pacote nativo, use: 
     ```
     savedesktop --import-config /caminho/para/nomedoarquivo.sd.tar.gz
     ```

**Nota**:
- em vez de `/caminho/para/nomedoarquivo.sd.tar.gz`, insira o caminho para o arquivo de configuração que você deseja importar, por exemplo: `/home/usuário/Downloads/minhaconfiguração.sd.tar.gz`

_Se você tiver quaisquer questões, pode usar as issues do GitHub._

{% include footer.html %}
