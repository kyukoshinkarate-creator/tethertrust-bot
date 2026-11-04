import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv(
    "8655862466:AAFhuKFPMaeqs1752ovXUEZ3xL8gft_JVHA"
)


CHANNEL_ID = os.getenv(
    "CHANNEL_ID",
    "@NovaExchangeIR"
)


SUPPORT_ID = os.getenv(
    "SUPPORT_ID",
    "@atefe_acc"
)


HISTORY_FILE = "history.json"


PRICE_INTERVAL = 15
