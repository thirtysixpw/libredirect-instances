import json
from pathlib import Path
from typing import Final

URL_START_REGEX = r"https?:\/{2}(?:[^\s\/]+\.)*"
URL_END_REGEX = "(?:\\/[^\\s\\/]+)*\\/?"
TOR_REGEX = URL_START_REGEX + "onion" + URL_END_REGEX
I2P_REGEX = URL_START_REGEX + "i2p" + URL_END_REGEX
LOKI_REGEX = URL_START_REGEX + "loki" + URL_END_REGEX
AUTH_REGEX = r"https?:\/{2}\S+:\S+@(?:[^\s\/]+\.)*[a-zA-Z0-9]+" + URL_END_REGEX

ROOT_DIR = Path(__file__).parent.parent
DATA_FILE = ROOT_DIR / "data.json"
BLACKLIST_FILE = ROOT_DIR / "blacklist.json"
NETWORKS_FILE = ROOT_DIR / "networks.json"

NETWORKS: Final[tuple[str, ...]] = tuple(json.loads(NETWORKS_FILE.read_text()).keys())
TIMEOUT: Final[int] = 5
