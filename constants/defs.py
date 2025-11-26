import json
import os

# ---------------------------------------------------------
# API & CONNECTION SETTINGS
# ---------------------------------------------------------

OANDA_API_KEY = os.getenv("OANDA_API_KEY", "YOUR_API_KEY")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID", "YOUR_ACCOUNT_ID")
OANDA_URL = os.getenv("OANDA_URL", "https://api-fxpractice.oanda.com/v3")

HEADERS = {
    "Authorization": f"Bearer {OANDA_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------------
# GENERAL DEFINITIONS
# ---------------------------------------------------------

TIMEFRAMES = {
    "M1": 60,
    "M5": 300,
    "M15": 900,
    "M30": 1800,
    "H1": 3600
}

SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "settings.json"
)

# ---------------------------------------------------------
# SETTINGS LOADER
# ---------------------------------------------------------

def load_settings():
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)
