import json
from pathlib import Path

from colorama import Fore, Style

from services import INSTANCE_FETCHERS
from services.utils import (
    filter_cloudflare,
    filter_trailing_slash,
    idna_encode,
)

instances = {fetcher.frontend: fetcher.fetch() for fetcher in INSTANCE_FETCHERS}

instances = filter_trailing_slash(instances)
instances = idna_encode(instances)
blacklist = {"cloudflare": filter_cloudflare(instances)}

instances_json = json.dumps(instances, ensure_ascii=False, indent=2)
Path("data.json").write_text(instances_json)
print(Fore.BLUE + "wrote " + Style.RESET_ALL + "data.json")

blacklist_json = json.dumps(blacklist, ensure_ascii=False, indent=2)
Path("blacklist.json").write_text(blacklist_json)
print(Fore.BLUE + "wrote " + Style.RESET_ALL + "blacklist.json")
