import time
import traceback
from datetime import datetime

from modules.candle_manager import CandleManager
from modules.technical_manager import TechnicalManager
from modules.trade_manager import TradeManager
from modules.trade_risk_calculator import TradeRiskCalculator
from infrastructure.log_wrapper import get_logger
from constants import defs


class Bot:
    def __init__(self):
        self.logger = get_logger("bot")
        self.settings = defs.load_settings()

        self.candle_manager = CandleManager(self.logger)
        self.technical_manager = TechnicalManager(self.logger)
        self.trade_manager = TradeManager(self.logger)
        self.risk_calculator = TradeRiskCalculator(self.logger)

        self.pairs = self.settings["pairs"]
        self.cooldown = self.settings.get("cooldown", 60)
        self.logger.info(f"bot v7 initialised with {len(self.pairs)} pairs")

    def run(self):
        self.logger.info("bot v7 started")

        while True:
            for pair in self.pairs:
                try:
                    self.process_pair(pair)
                except Exception as e:
                    self.logger.error(f"process_pair({pair}) error: {e}")
                    self.logger.debug(traceback.format_exc())
            time.sleep(self.cooldown)

    def process_pair(self, pair):
        candles = self.candle_manager.get_candles(pair)
        if candles is None:
            self.logger.warning(f"no candles for {pair}")
            return

        signal = self.technical_manager.get_trade_signal(
            pair=pair,
            candles=candles,
            settings=self.settings["strategy"]
        )

        if signal is None:
            return

        units = self.risk_calculator.calculate_units(
            pair=pair,
            candles=candles,
            settings=self.settings["risk"]
        )

        if units is None:
            self.logger.warning(f"units calc skipped for {pair}")
            return

        result = self.trade_manager.execute_trade(
            pair=pair,
            signal=signal,
            units=units,
            settings=self.settings["strategy"]
        )

        if result:
            self.logger.info(f"{pair} trade executed: {result}")



if __name__ == "__main__":
    try:
        Bot().run()
    except KeyboardInterrupt:
        print("\nBot stopped by user.\n")
    except Exception as e:
        print(f"startup error: {e}")
        raise
