import asyncio
from datetime import datetime, timezone, timedelta

import jdatetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import PRICE_INTERVAL
from price_service import get_average_price
from history_manager import save_history, get_daily_stats
from alerts import create_alert
from morning_messages import get_morning_message
from telegram_service import telegram_service
from logger import logger


# -------------------------
# Tehran Time
# -------------------------
TEHRAN = timezone(timedelta(hours=3, minutes=30))


# -------------------------
# Last Price
# -------------------------
last_price = None


# -------------------------
# Date and Time
# -------------------------
def datetime_now():
    now = datetime.now(TEHRAN)
    jalali = jdatetime.datetime.fromgregorian(datetime=now)
    return f"{jalali.strftime('%Y/%m/%d')} - {now.strftime('%H:%M')}"


# -------------------------
# Send Price Report
# -------------------------
async def send_price_report():
    global last_price

    try:
        result = await get_average_price()

        if not result:
            logger.warning("No price received")
            return

        current_price = result["price"]
        sources = result["sources"]

        change_amount = 0
        change_percent = 0.0

        if last_price:
            change_amount = current_price - last_price
            change_percent = (change_amount / last_price) * 100

        sell_price = current_price + 150
        buy_price = current_price

        save_history(
            current_price,
            sell_price,
            sources,
            change_amount,
            change_percent,
        )

        now = datetime_now()
        message = f"""💠 NovaX Exchange | قیمت لحظه‌ای 💠
🟢 خرید:
{buy_price:,.0f} تومان
🔴 فروش:
{sell_price:,.0f} تومان
{change_amount:+,.0f} تومان ({change_percent:+.2f}%)
🕒 {now}
"""

        await telegram_service.send_message(message)

        if last_price:
            alert = create_alert(current_price, last_price)
            if alert:
                await telegram_service.send_message(alert)

        last_price = current_price
        logger.info("Price sent successfully")

    except Exception:
        logger.exception("Error while sending price report")


# -------------------------
# Morning Report
# -------------------------
async def send_morning_report():
    try:
        message = get_morning_message()
        if message:
            await telegram_service.send_message(message)
            logger.info("Morning report sent")
    except Exception:
        logger.exception("Error while sending morning report")


# -------------------------
# Night Report
# -------------------------
async def send_night_report():
    try:
        stats = get_daily_stats()

        if not stats:
            logger.warning("No daily stats available")
            return

        message = f"""💠 TETHERTRUST | گزارش روزانه

┏━━━━━━━━━━┓

📊 آمار امروز بازار تتر

💵 شروع:
{stats["first"]:,.0f} تومان

🔵 پایان:
{stats["last"]:,.0f} تومان

⬆️ بالاترین:
{stats["high"]:,.0f} تومان

⬇️ پایین‌ترین:
{stats["low"]:,.0f} تومان

📈 تغییر روز:
{stats["change"]:+,.0f} تومان

({stats["percent"]:+.2f}%)

📌 میانگین:
{stats["average"]:,.0f} تومان

⚜️ اعتبار، ارزِ ماندگارِ ماست.

📢 کانال رسمی: @NovaExchangeIR
🎧 پشتیبانی: @atefe_acc

┗━━━━━━━━━━┛
"""

        await telegram_service.send_message(message)
        logger.info("Night report sent")

    except Exception:
        logger.exception("Error while sending night report")


# -------------------------
# Main Runner
# -------------------------
async def main():
    logger.info("Starting TetherTrust Bot...")

    scheduler = AsyncIOScheduler(timezone=TEHRAN)

    scheduler.add_job(
        send_price_report,
        "interval",
        minutes=PRICE_INTERVAL,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        send_morning_report,
        "cron",
        hour=7,
        minute=59,
    )

    scheduler.add_job(
        send_night_report,
        "cron",
        hour=23,
        minute=59,
    )

    scheduler.start()

    # Send one price report immediately when the bot starts.
    await send_price_report()

    logger.info("TetherTrust Bot is running")

    while True:
        await asyncio.sleep(60)


# -------------------------
# Start Program
# -------------------------
if __name__ == "__main__":
    asyncio.run(main())
