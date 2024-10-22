from .base import InstanceFetcher


class Libreddit(InstanceFetcher):
    frontend = "libreddit"
    url = "https://github.com/libreddit/libreddit-instances/raw/master/instances.json"
    network_mapping = {"clearnet": "url", "tor": "onion", "i2p": "i2p"}
    keys = ["instances"]


class Redlib(InstanceFetcher):
    frontend = "redlib"
    url = "https://github.com/redlib-org/redlib-instances/raw/main/instances.json"
    network_mapping = {"clearnet": "url", "tor": "onion", "i2p": "i2p"}
    keys = ["instances"]


class Teddit(InstanceFetcher):
    frontend = "teddit"
    url = "https://codeberg.org/teddit/teddit/raw/branch/main/instances.json"
    network_mapping = {"clearnet": "url", "tor": "onion", "i2p": "i2p"}
