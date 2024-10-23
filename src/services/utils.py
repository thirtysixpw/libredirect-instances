import socket
from typing import Any
from urllib.parse import urlparse

import requests
from colorama import Fore, Style

from ..constants import TIMEOUT


def get_cloudflare_ips() -> list[str]:
    data = requests.get("https://www.cloudflare.com/ips-v4", timeout=TIMEOUT).text
    return data.split("\n")


CLOUDFLARE_IPS = get_cloudflare_ips()


def ip2bin(ip: str) -> str:
    return "".join(map(str, [f"{int(x):08b}" for x in ip.split(".")]))


def is_cloudflare(url: str) -> bool:
    try:
        hostname = urlparse(url).hostname
        if hostname is None:
            return False
        instance_ip = socket.gethostbyname(hostname)
        if instance_ip is None:
            return False
    except Exception:
        return False
    instance_bin = ip2bin(instance_ip)

    for cloudflare_ip_mask in CLOUDFLARE_IPS:
        cloudflare_ip = cloudflare_ip_mask.split("/")[0]
        cloudflare_bin = ip2bin(cloudflare_ip)

        mask = int(cloudflare_ip_mask.split("/")[1])
        cloudflare_bin_masked = cloudflare_bin[:mask]
        instance_bin_masked = instance_bin[:mask]

        if cloudflare_bin_masked == instance_bin_masked:
            print(url + " is behind " + Fore.RED + "cloudflare" + Style.RESET_ALL)
            return True
    return False


def filter_cloudflare(instances: dict[str, Any]) -> list[str]:
    cloudflare = []
    for frontend, networks in instances.items():
        for network in networks:
            for url in instances[frontend][network]:
                if not is_valid_url(url):
                    instances[frontend][network].remove(url)
                    print("removed " + url)
                elif (
                    not url.endswith(".onion")
                    and not url.endswith(".i2p")
                    and not url.endswith(".loki")
                    and is_cloudflare(url)
                ):
                    cloudflare.append(url)
    return cloudflare


def filter_trailing_slash(instances: dict[str, Any]) -> dict[str, Any]:
    res = {}
    for frontend, networks in instances.items():
        res[frontend] = {}
        for network in networks:
            res[frontend][network] = []
            for url in instances[frontend][network]:
                if url.endswith("/"):
                    res[frontend][network].append(url[:-1])
                    print(Fore.YELLOW + "Fixed " + Style.RESET_ALL + url)
                else:
                    res[frontend][network].append(url)
    return res


def idna_encode(instances: dict[str, Any]) -> dict[str, Any]:
    res = {}
    for frontend, networks in instances.items():
        res[frontend] = {}
        for network in networks:
            res[frontend][network] = []
            for url in instances[frontend][network]:
                try:
                    encoded_url = url.encode("idna").decode("utf8")
                    res[frontend][network].append(encoded_url)
                    if encoded_url != url:
                        print(Fore.YELLOW + "Fixed " + Style.RESET_ALL + url)
                except Exception:
                    res[frontend][network].append(url)
    return res


def is_valid_url(url: str):  # by avanitrachhadiya2155
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
