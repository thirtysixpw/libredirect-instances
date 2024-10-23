import json

from colorama import Fore, Style

from .constants import BLACKLIST_FILE, DATA_FILE
from .services import INSTANCE_FETCHERS
from .services.utils import (
    filter_cloudflare,
    filter_trailing_slash,
    idna_encode,
)


def main() -> None:
    instances = {fetcher.frontend: fetcher.get_instances() for fetcher in INSTANCE_FETCHERS}

    instances = filter_trailing_slash(instances)
    instances = idna_encode(instances)
    blacklist = {"cloudflare": filter_cloudflare(instances)}

    instances_json = json.dumps(instances, ensure_ascii=False, indent=2)
    DATA_FILE.write_text(instances_json)
    print(f"{Fore.BLUE}wrote{Style.RESET_ALL} {DATA_FILE.name}")

    blacklist_json = json.dumps(blacklist, ensure_ascii=False, indent=2)
    BLACKLIST_FILE.write_text(blacklist_json)
    print(f"{Fore.BLUE}wrote{Style.RESET_ALL} {BLACKLIST_FILE.name}")


if __name__ == "__main__":
    main()
