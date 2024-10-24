from .base import FixedInstanceFetcher


class OSM(FixedInstanceFetcher):
    frontend = "osm"


class Neuters(FixedInstanceFetcher):
    frontend = "neuters"


class Wikiless(FixedInstanceFetcher):
    frontend = "wikiless"


class MikuInvidious(FixedInstanceFetcher):
    frontend = "mikuInvidious"


class Twineo(FixedInstanceFetcher):
    frontend = "twineo"


class CloudTube(FixedInstanceFetcher):
    frontend = "cloudtube"


class SimplyTranslate(FixedInstanceFetcher):
    frontend = "simplyTranslate"
