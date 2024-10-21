import logging
import re
import traceback
from typing import Any

import requests
import yaml
from colorama import Fore, Style

from .base import I2P_REGEX, TIMEOUT, TOR_REGEX, InstanceFetcher
from .utils import fetch_cache


class SearXNG(InstanceFetcher):
    frontend = "searxng"
    url = "https://searx.space/data/instances.json"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).json()

            for item in raw_data["instances"]:
                if (
                    re.search(TOR_REGEX, item[:-1])
                    and raw_data["instances"][item].get("generator") == "searxng"
                ):
                    instances["tor"].append(item[:-1])
                elif (
                    re.search(I2P_REGEX, item[:-1])
                    and raw_data["instances"][item].get("generator") == "searxng"
                ):
                    instances["i2p"].append(item[:-1])
                elif raw_data["instances"][item].get("generator") == "searxng":
                    instances["clearnet"].append(item[:-1])

            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class Searx(InstanceFetcher):
    frontend = "searx"
    url = "https://raw.githubusercontent.com/searx/searx-instances/master/searxinstances/instances.yml"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).text
            data = yaml.safe_load(raw_data)

            for key in data:
                instances["clearnet"].append(key)
                if "additional_urls" in data[key]:
                    for additional_url in data[key]["additional_urls"]:
                        if data[key]["additional_urls"][additional_url] == "Hidden Service":
                            instances["tor"].append(additional_url)

            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class Whoogle(InstanceFetcher):
    frontend = "whoogle"
    url = "https://raw.githubusercontent.com/benbusby/whoogle-search/main/README.md"
    regex = r"\| \[https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+\]\((https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\) \| "


class LibreX(InstanceFetcher):
    frontend = "librex"
    url = "https://raw.githubusercontent.com/hnhx/librex/main/instances.json"
    network_mapping = {"clearnet": "clearnet", "tor": "tor", "i2p": "i2p"}
    keys = ["instances"]
