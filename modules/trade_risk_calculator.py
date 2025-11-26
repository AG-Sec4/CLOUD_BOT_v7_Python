import traceback


class TradeRiskCalculator:
    def __init__(self, logger):
        self.logger = logger

    def calculate_units(self, pair, candles, settings):
        try:
            balance = settings["account_balance"]
            max_risk = settings["max_risk_per_trade"]

            stop_loss = settings["stop_loss"]

            pip_value = 0.10  # simplified example
            risk_value = max_risk

            units = int(risk_value / (pip_value * stop_loss))

            units = max(units, settings["min_units"])
            units = min(units, settings["max_units"])

            return units

        except Exception:
            self.logger.error(f"risk_calc error for {pair}")
            self.logger.debug(traceback.format_exc())
            return None
