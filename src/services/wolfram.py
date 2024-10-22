import json
import logging
import traceback
from typing import Any

import requests
from colorama import Fore, Style

from ..constants import TIMEOUT
from .base import InstanceFetcher


class WolfreeAlpha(InstanceFetcher):
    frontend = "wolfreeAlpha"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        wolfree_instances = [
            "https://gqq.gitlab.io",
            "https://jqq.gitlab.io",
            "https://rqq.gitlab.io",
            "https://sqq.gitlab.io",
            "https://uqq.gitlab.io",
        ]
        for instance in wolfree_instances:
            try:
                r = requests.get(instance + "/instances.json", timeout=TIMEOUT)
                if r.status_code != 200:
                    continue
                raw_data = json.loads(r.text)
                networks = raw_data["wolfree"]
                instances = {}
                for i in networks:
                    instances[i] = networks[i]
                print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
                return instances
            except Exception:
                logging.error(traceback.format_exc())
        return {"clearnet": wolfree_instances}
