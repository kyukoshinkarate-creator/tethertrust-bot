import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)


CHANNEL_ID = os.getenv(
    "CHANNEL_ID",
    "@Usdt_irrr"
)


SUPPORT_ID = os.getenv(
    "SUPPORT_ID",
    "@Mhd_sorena"
)


HISTORY_FILE = "history.json"


PRICE_INTERVAL = 15
