import re
from typing import Any

import pandas

from .base import InstanceFetcher


class PixivFE(InstanceFetcher):
    frontend = "pixivFe"
    url = "https://gitlab.com/pixivfe/pixivfe-docs/-/raw/master/data/instances.csv?ref_type=heads"

    @classmethod
    def fetch(cls) -> dict[str, Any]:
        df = pandas.read_csv(cls.url)

        clearnet = []
        for value in df["URL"]:
            r = re.findall(r"\((.*?)\)", value)
            if r:
                clearnet.append(r[0])

        return {"clearnet": clearnet, "tor": [], "i2p": [], "loki": []}
