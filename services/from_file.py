from .base import InstanceFetcher


class OSM(InstanceFetcher):
    frontend = "osm"
    is_fixed = True


class Neuters(InstanceFetcher):
    frontend = "neuters"
    is_fixed = True


class Wikiless(InstanceFetcher):
    frontend = "wikiless"
    is_fixed = True


class MikuInvidious(InstanceFetcher):
    frontend = "mikuInvidious"
    is_fixed = True


class Twineo(InstanceFetcher):
    frontend = "twineo"
    is_fixed = True


class CloudTube(InstanceFetcher):
    frontend = "cloudtube"
    is_fixed = True


class SimplyTranslate(InstanceFetcher):
    frontend = "simplyTranslate"
    is_fixed = True
