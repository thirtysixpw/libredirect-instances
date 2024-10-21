import logging
import re
import traceback
from typing import Any

import requests
from colorama import Fore, Style

from .base import TIMEOUT, InstanceFetcher
from .utils import fetch_cache


class Tent(InstanceFetcher):
    frontend = "tent"
    url = "https://forgejo.sny.sh/sun/Tent/raw/branch/main/instances.json"
    network_mapping = {"clearnet": "url"}


class RuralDictionary(InstanceFetcher):
    frontend = "ruralDictionary"
    url = "https://codeberg.org/zortazert/rural-dictionary/raw/branch/master/instances.json"
    network_mapping = {"clearnet": "clearnet", "tor": "tor", "i2p": "i2p"}


class Laboratory(InstanceFetcher):
    frontend = "laboratory"
    url = "https://git.vitali64.duckdns.org/utils/laboratory.git/plain/README.md"
    regex = r"\| (https:\/{2}.*?) \|"


class GotHub(InstanceFetcher):
    frontend = "gothub"
    url = "https://codeberg.org/gothub/gothub-instances/raw/branch/master/instances.json"
    network_mapping = {"clearnet": "link"}


class BiblioReads(InstanceFetcher):
    frontend = "biblioReads"
    url = "https://raw.githubusercontent.com/nesaku/BiblioReads/main/instances.json"
    network_mapping = {"clearnet": "url", "tor": "onion", "i2p": "i2p"}


class Libremdb(InstanceFetcher):
    frontend = "libremdb"
    url = "https://raw.githubusercontent.com/zyachel/libremdb/main/instances.json"
    network_mapping = {"clearnet": "clearnet", "tor": "tor", "i2p": "i2p"}


class BreezeWiki(InstanceFetcher):
    frontend = "breezeWiki"
    url = "https://docs.breezewiki.com/files/instances.json"
    network_mapping = {"clearnet": "instance"}


class Binternet(InstanceFetcher):
    frontend = "binternet"
    url = "https://raw.githubusercontent.com/Ahwxorg/Binternet/main/README.md"
    regex = r"\| \[[\w\.]+!?\]\((https?:\/{2}(?:\S+\.)+[a-zA-Z0-9]*)\/?\)"


class Dumb(InstanceFetcher):
    frontend = "dumb"
    url = "https://raw.githubusercontent.com/rramiachraf/dumb/main/instances.json"
    network_mapping = {"clearnet": "clearnet", "tor": "tor", "i2p": "i2p"}


class Suds(InstanceFetcher):
    frontend = "suds"
    url = "https://git.vern.cc/cobra/Suds/raw/branch/main/instances.json"
    network_mapping = {"clearnet": "clearnet", "tor": "tor", "i2p": "i2p"}


class Proxigram(InstanceFetcher):
    frontend = "proxigram"
    url = "https://codeberg.org/proxigram/proxigram/wiki/raw/Instances.md"
    regex = r"\[(https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\]"


class Rimgo(InstanceFetcher):
    frontend = "rimgo"
    url = "https://rimgo.codeberg.page/api.json"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).json()
            for instance in raw_data["clearnet"]:
                instances["clearnet"].append(instance["url"])

            for instance in raw_data["tor"]:
                instances["tor"].append(instance["url"])

            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


# class Jitsi(FrontendInstances):
#         name="jitsi"
#         url= "https://raw.githubusercontent.com/jitsi/handbook/master/docs/community/instances.md"
#         regex=r"\|(?:(?: |	)+)+((?:[a-z]+\.)+[a-z]+)(?:(?: |	)+)+\|"
#
#     FrontendInstances["jitsi"]["clearnet"] = list(
#         map(lambda x: "https://" + x, FrontendInstances["jitsi"]["clearnet"])
#
#     FrontendInstances["jitsi"]["clearnet"].insert(0, "https://8x8.vc")
#     FrontendInstances["jitsi"]["clearnet"].insert(0, "https://meet.jit.si")


class AnonymousOverflow(InstanceFetcher):
    frontend = "anonymousOverflow"
    url = "https://raw.githubusercontent.com/httpjamesm/AnonymousOverflow/main/instances.json"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).json()
            for net_type, x_instances in raw_data.items():
                x_res = [x["url"].strip("/") for x in x_instances]
                instances[
                    {"clearnet": "clearnet", "onion": "tor", "i2p": "i2p", "loki": "loki"}[
                        net_type
                    ]
                ] = x_res
            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class ProxiTok(InstanceFetcher):
    frontend = "proxiTok"
    url = "https://raw.githubusercontent.com/wiki/pablouser1/ProxiTok/Public-instances.md"
    regex = r"\| \[.*\]\(([-a-zA-Z0-9@:%_\+.~#?&//=]{2,}\.[a-z]{2,}\b(?:\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)\)(?: \(Official\))? +\|(?:(?: [A-Z]*.*\|.*\|)|(?:$))"


class Priviblur(InstanceFetcher):
    frontend = "priviblur"
    url = "https://raw.githubusercontent.com/syeopite/priviblur/master/instances.md"
    regex = r"\| ?\[.*\]\((https?:\/{2}(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\) ?|"


class SafeTwitch(InstanceFetcher):
    frontend = "safetwitch"
    url = "https://codeberg.org/dragongoose/safetwitch/raw/branch/master/README.md"
    regex = re.compile(
        r"^\| \[.*?\]\((https?:\/{2}(?:[^\s\/]+\.)*(?:[^\s\/]+\.)+[a-zA-Z0-9]+)\/?\)", re.MULTILINE
    )


class Nitter(InstanceFetcher):
    frontend = "nitter"
    url = "https://raw.githubusercontent.com/wiki/zedeus/nitter/Instances.md"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).text

            public = re.findall(r"## Public((?:\n|.*)+?)##", raw_data)
            if public:
                for line in public[0].split("\n"):
                    result = re.findall(r"^\| \[.*?\]\((https.*?)\)", line)
                    if len(result) > 0:
                        instances["clearnet"].append(result[0])

            public = re.findall(r"## Tor((?:\n|.*)+?)##", raw_data)
            if public:
                for line in public[0].split("\n"):
                    result = re.findall(r"^\| <(http.*?)\/?>", line)
                    if len(result) > 0:
                        instances["tor"].append(result[0])

            public = re.findall(r"## I2P((?:\n|.*)+?)##", raw_data)
            if public:
                for line in public[0].split("\n"):
                    result = re.findall(r"^- <(http.*?)\/?>", line)
                    if len(result) > 0:
                        instances["i2p"].append(result[0])

            public = re.findall(r"## Lokinet((?:\n|.*)+?)##", raw_data)
            if public:
                for line in public[0].split("\n"):
                    result = re.findall(r"^- <(http.*?)\/?>", line)
                    if len(result) > 0:
                        instances["loki"].append(result[0])

            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class Send(InstanceFetcher):
    frontend = "send"
    url = "https://gitlab.com/timvisee/send-instances/-/raw/master/README.md"
    regex = r"(https.*?) \|.*?\n"


class Quetre(InstanceFetcher):
    frontend = "quetre"
    url = "https://raw.githubusercontent.com/zyachel/quetre/main/instances.json"
    network_mapping = {"clearnet": "clearnet", "tor": "tor", "i2p": "i2p"}


class PrivateBin(InstanceFetcher):
    frontend = "privateBin"
    url = "https://privatebin.info/directory/api?top=100&https_redirect=true&min_rating=A&csp_header=true&min_uptime=100&attachments=true"
    network_mapping = {"clearnet": "url"}


class SkunkyArt(InstanceFetcher):
    frontend = "skunkyArt"
    url = "https://git.macaw.me/skunky/SkunkyArt/raw/branch/master/instances.json"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        instances = {"clearnet": [], "tor": [], "i2p": [], "loki": []}
        try:
            raw_data = requests.get(cls.url, timeout=TIMEOUT).json()
            clearnet = []
            for item in raw_data["instances"]:
                if "clearnet" in item["urls"]:
                    clearnet.append(item["urls"]["clearnet"])
            instances["clearnet"] = clearnet
            print(Fore.GREEN + "Fetched " + Style.RESET_ALL + cls.frontend)
        except Exception:
            fetch_cache(cls.frontend, instances)
            logging.error(traceback.format_exc())
        return instances


class Koub(InstanceFetcher):
    frontend = "koub"
    url = "https://codeberg.org/gospodin/koub/raw/branch/master/instances.json"
    network_mapping = {"clearnet": "url"}


class TransLite(InstanceFetcher):
    frontend = "transLite"
    url = "https://codeberg.org/gospodin/translite/raw/branch/master/instances.json"
    network_mapping = {"clearnet": "url"}
