from .base import InstanceFetcher


class LinvgaTranslate(InstanceFetcher):
    frontend = "lingva"
    url = "https://raw.githubusercontent.com/TheDavidDelta/lingva-translate/main/instances.json"


class LibreTranslate(InstanceFetcher):
    frontend = "libreTranslate"
    url = "https://raw.githubusercontent.com/LibreTranslate/LibreTranslate/main/README.md"
    regex = r"\[(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/\/(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\)"


class Mozhi(InstanceFetcher):
    frontend = "mozhi"
    url = "https://codeberg.org/aryak/mozhi/raw/branch/master/instances.json"
    network_mapping = {"clearnet": "link", "tor": "onion", "i2p": "i2p"}
