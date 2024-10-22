import json
import re
from pathlib import Path
from typing import Any

import requests
from colorama import Fore, Style

from ..constants import DATA_FILE, I2P_REGEX, LOKI_REGEX, NETWORKS, TIMEOUT, TOR_REGEX


class InstanceFetcher:
    frontend: str
    url: str
    regex: str | re.Pattern[str] | None = None
    keys: list[str] | None = None
    network_mapping: dict[str, str] | None = None
    is_fixed: bool = False

    @classmethod
    def _parse_instance_url(cls, instances: dict[str, Any], url: str) -> None:
        if not url.strip():
            return
        if re.search(TOR_REGEX, url):
            instances["tor"].append(url)
        elif re.search(I2P_REGEX, url):
            instances["i2p"].append(url)
        elif re.search(LOKI_REGEX, url):
            instances["loki"].append(url)
        else:
            instances["clearnet"].append(url)

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {network: [] for network in NETWORKS}
        try:
            if cls.regex:
                raw_data = requests.get(cls.url, timeout=TIMEOUT).text
                for url in re.findall(cls.regex, raw_data):
                    cls._parse_instance_url(instances, url)
            elif cls.is_fixed:
                raw_data = Path(f"fixed/{cls.frontend}.json").read_text()
                instances = json.loads(raw_data)
            else:
                raw_data = requests.get(cls.url, timeout=TIMEOUT).json()
                if cls.keys is not None:
                    for key in cls.keys:
                        raw_data = raw_data[key]
                for item in raw_data:
                    if cls.network_mapping is not None:
                        for network in NETWORKS:
                            if (
                                (mapping := cls.network_mapping.get(network)) is not None
                                and mapping in item
                                and item[mapping] is not None
                            ):
                                if isinstance(item[mapping], list):
                                    for instance in item[mapping]:
                                        if instance.strip():
                                            instances[network].append(instance)
                                elif instance := item[mapping].strip():
                                    instances[network].append(instance)
                    else:
                        cls._parse_instance_url(instances, item)
            print(f"{Fore.GREEN}Fetched{Style.RESET_ALL} {cls.frontend}")
            return instances
        except (
            requests.exceptions.Timeout,
            requests.exceptions.JSONDecodeError,
            requests.exceptions.ConnectionError,
        ):
            print(f"{Fore.YELLOW}Failed{Style.RESET_ALL} to fetch {cls.frontend}")
            try:
                instances = json.loads(DATA_FILE.read_text())[cls.frontend]
                print(f"{Fore.GREEN}Loaded{Style.RESET_ALL} cached {cls.frontend}")
                return instances
            except (UnicodeDecodeError, KeyError):
                print(f"{Fore.RED}Failed{Style.RESET_ALL} to get cached {cls.frontend}")
                return {}
