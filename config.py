import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")


CHANNEL_ID = os.getenv(
    "CHANNEL_ID",
    "@NovaExchangeIR"
)


SUPPORT_ID = os.getenv(
    "SUPPORT_ID",
    "@atefe_acc"
)


HISTORY_FILE = "history.json"


PRICE_INTERVAL = 10
