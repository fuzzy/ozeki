import urllib.request
import urllib.parse
import json
import os
from datetime import datetime, timedelta


class SumoAPI:
    BASE_URL = "https://sumo-api.com/api"
    CACHE_DIR = f'{os.getenv("HOME", None)}/.cache/ozeki'

    def __init__(self):
        if not os.path.isdir(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR, exist_ok=True)

    def _get(self, path, params=None):
        url = f"{self.BASE_URL}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"HTTP {resp.status}")
                return json.load(resp)
        except Exception as e:
            raise RuntimeError(f"Failed to GET {url}: {e}")

    def _cache(self, fn, uri):
        if os.path.isfile(fn):
            mtime = datetime.fromtimestamp(os.path.getmtime(fn))
            if datetime.now() - mtime < timedelta(hours=1):
                return json.loads(open(fn, "r").read())

        retv = self._get(uri)
        if not os.path.isdir(os.path.dirname(fn)):
            os.makedirs(os.path.dirname(fn))
        with open(fn, "w+") as fp:
            fp.write(json.dumps(retv, default=str, indent=2))
        return retv

    def rikishis(self):
        return self._cache(f"{self.CACHE_DIR}/rikishis.json", "/rikishis")

    def rikishi(self, rikishi_id):
        return self._cache(
            f"{self.CACHE_DIR}/rikishi/{rikishi_id}/rikihsi.json",
            f"/rikishi/{rikishi_id}",
        )

    def rikishi_stats(self, rikishi_id):
        return self._cache(
            f"{self.CACHE_DIR}/rikishi/{rikishi_id}/stats.json",
            f"/rikishi/{rikishi_id}/stats",
        )

    def rikishi_matches(self, rikishi_id):
        return self._cache(
            f"{self.CACHE_DIR}/rikishi/{rikishi_id}/matches.json",
            f"/rikishi/{rikishi_id}/matches",
        )

    def basho(self, basho_id):
        return self._cache(
            f"{self.CACHE_DIR}/basho_{basho_id}.json", f"/basho/{basho_id}"
        )

    def banzuke(self, basho_id, division):
        return self._cache(
            f"{self.CACHE_DIR}/basho/{basho_id}/banzuke_{division}.json",
            f"/basho/{basho_id}/banzuke/{division}",
        )

    def torikumi(self, basho_id, division, day):
        try:
            return self._cache(
                f"{self.CACHE_DIR}/basho/{basho_id}/torikumi/{division}/{day}.json",
                f"/basho/{basho_id}/torikumi/{division}/{day}",
            )
        except Exception:
            return {}
