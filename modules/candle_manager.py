import requests
import traceback
from constants import defs


class CandleManager:
    def __init__(self, logger):
        self.logger = logger
        self.url = defs.OANDA_URL

    def get_candles(self, pair):
        """fetch latest candles for instrument"""
        try:
            params = {
                "count": 200,
                "granularity": defs.load_settings()["granularity"]
            }

            endpoint = f"{self.url}/instruments/{pair}/candles"
            r = requests.get(endpoint, headers=defs.HEADERS, params=params)

            if r.status_code != 200:
                self.logger.error(
                    f"{pair} candle error status {r.status_code}: {r.text}"
                )
                return None

            data = r.json().get("candles", [])
            if not data:
                self.logger.warning(f"{pair} returned no candles")
                return None

            candles = [
                float(c["mid"]["c"]) for c in data if c.get("complete")
            ]

            if len(candles) < 50:
                self.logger.warning(f"{pair} not enough candles")
                return None

            return candles

        except Exception:
            self.logger.error(f"candle_manager exception for {pair}")
            self.logger.debug(traceback.format_exc())
            return None
