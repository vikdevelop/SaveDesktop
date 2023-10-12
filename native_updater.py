import requests

response = requests.get("https://api.github.com/repos/vikdevelop/SaveDesktop/releases/latest")
github_version = response.json()["name"]

from localization import *

d_ver = version.replace("-native", "")

if not d_ver >= f"{github_version}":
    os.system("git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop && sh /tmp/SaveDesktop/install_native.sh --remove")
    os.system("git clone https://github.com/vikdevelop/SaveDesktop /tmp/SaveDesktop && sh /tmp/SaveDesktop/install_native.sh --install")
