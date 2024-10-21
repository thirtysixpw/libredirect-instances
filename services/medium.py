from .base import InstanceFetcher


class Scribe(InstanceFetcher):
    frontend = "scribe"
    url = "https://git.sr.ht/~edwardloveall/scribe/blob/main/docs/instances.json"


class LibMedium(InstanceFetcher):
    frontend = "libMedium"
    url = "https://raw.githubusercontent.com/realaravinth/libmedium/master/README.md"
    regex = r"\| (https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/? +\|"
