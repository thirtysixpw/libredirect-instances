import logging
import re
import traceback
from typing import Any

import requests
from colorama import Fore, Style

from .base import TIMEOUT, InstanceFetcher
from .utils import fetch_cache


class Invidious(InstanceFetcher):
    frontend = "invidious"
    url = "https://api.invidious.io/instances.json"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).json()
            for instance in raw_data:
                if instance[1]["type"] == "https":
                    instances["clearnet"].append(instance[1]["uri"])
                elif instance[1]["type"] == "onion":
                    instances["tor"].append(instance[1]["uri"])
                elif instance[1]["type"] == "i2p":
                    instances["i2p"].append(instance[1]["uri"])
            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
            return instances
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class Piped(InstanceFetcher):
    frontend = "piped"
    url = "https://raw.githubusercontent.com/wiki/TeamPiped/Piped/Instances.md"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).text

            tmp = re.findall(r" \| (https:\/{2}(?:[^\s\/]+\.)+[a-zA-Z]+) \| ", raw_data)
            for item in tmp:
                try:
                    print(Fore.GREEN + "Fetching " + Style.RESET_ALL + item, end=" ")
                    url = requests.get(item, timeout=5).url
                    if url.strip("/") == item:
                        print(Fore.RED + "𐄂")
                        continue
                    print(Fore.GREEN + "✓")
                    instances["clearnet"].append(url)
                except Exception:
                    print(Fore.RED + "𐄂")
                    continue
            instances["clearnet"].remove("https://piped.video")
            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class Materialious(InstanceFetcher):
    frontend = "materialious"
    url = "https://raw.githubusercontent.com/Materialious/Materialious/main/docs/INSTANCES.md"
    regex = r"- \[.*\]\((https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\)"


class PipedMaterial(InstanceFetcher):
    frontend = "pipedMaterial"
    url = "https://raw.githubusercontent.com/mmjee/Piped-Material/master/README.md"
    regex = r"\| (https?:\/{2}(?:\S+\.)+[a-zA-Z0-9]*) +\| Production"


class Poketube(InstanceFetcher):
    frontend = "poketube"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(
                "https://codeberg.org/Ashley/poketube/raw/branch/main/instances.json",
                timeout=TIMEOUT,
            ).json()
            for element in raw_data:
                instances["clearnet"].append(element[1]["uri"])

            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
            return instances
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class Hyperpipe(InstanceFetcher):
    frontend = "hyperpipe"
    url = "https://codeberg.org/Hyperpipe/pages/raw/branch/main/api/frontend.json"
    network_mapping = {"clearnet": "url"}
