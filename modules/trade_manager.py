import requests
import traceback
from constants import defs


class TradeManager:
    def __init__(self, logger):
        self.logger = logger
        self.url = defs.OANDA_URL

    def execute_trade(self, pair, signal, units, settings):
        try:
            side = "buy" if signal == "BUY" else "sell"

            payload = {
                "order": {
                    "instrument": pair,
                    "units": str(units if side == "buy" else -units),
                    "type": "MARKET",
                    "timeInForce": "FOK",
                    "positionFill": "DEFAULT"
                }
            }

            endpoint = f"{self.url}/accounts/{defs.OANDA_ACCOUNT_ID}/orders"
            r = requests.post(endpoint, json=payload, headers=defs.HEADERS)

            if r.status_code != 201:
                self.logger.error(f"{pair} trade error {r.status_code}: {r.text}")
                return None

            return r.json()

        except Exception:
            self.logger.error(f"trade_manager exception for {pair}")
            self.logger.debug(traceback.format_exc())
            return None
