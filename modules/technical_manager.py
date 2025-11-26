import numpy as np
import traceback


class TechnicalManager:
    def __init__(self, logger):
        self.logger = logger

    def get_trade_signal(self, pair, candles, settings):
        try:
            prices = np.array(candles, dtype=float)

            ma_period = settings["ma_period"]
            std_period = settings["std_period"]
            std_mult = settings["std_multiplier"]

            if len(prices) <= ma_period:
                return None

            ma = prices[-ma_period:].mean()
            std = prices[-std_period:].std()

            upper = ma + std * std_mult
            lower = ma - std * std_mult

            last = prices[-1]

            if last < lower:
                return "BUY"

            if last > upper:
                return "SELL"

            return None

        except Exception:
            self.logger.error(f"technical_manager error for {pair}")
            self.logger.debug(traceback.format_exc())
            return None
