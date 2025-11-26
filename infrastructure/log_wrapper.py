import logging
import os
from datetime import datetime


LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "logs"
)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_logger(name: str):
    """creates a simple, daily-rotating logger"""

    date_str = datetime.utcnow().strftime("%Y%m%d")
    logfile = os.path.join(LOG_DIR, f"main_{date_str}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(logfile)
        sh = logging.StreamHandler()

        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        fh.setFormatter(fmt)
        sh.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger
