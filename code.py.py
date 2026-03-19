import requests
from bs4 import BeautifulSoup
import schedule
import time
from telegram import Bot

# ====== CONFIG ======
BOT_TOKEN = "8337254899:AAGcUk0FN7BDDM6GUgupuDJzd55f8OKTpxE"
CHAT_ID = 1467665974

bot = Bot(token=BOT_TOKEN)

# ====== FUNCTION ======
def check_news():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr", class_="calendar__row")

    for row in rows:
        try:
            impact = row.find("td", class_="calendar__impact").text.strip()
            currency = row.find("td", class_="calendar__currency").text.strip()
            event = row.find("td", class_="calendar__event").text.strip()
            time_news = row.find("td", class_="calendar__time").text.strip()

            if "High" in impact and currency == "USD":
                message = f"""
🚨 HIGH IMPACT NEWS ALERT 🚨

Currency: {currency}
Event: {event}
Time: {time_news}

⚠️ Prepare for volatility in:
XAUUSD / BTCUSD / ETHUSD

Plan:
Wait for liquidity sweep
Trade after displacement (SMC)
"""
                bot.send_message(chat_id=CHAT_ID, text=message)

        except:
            continue

# ====== SCHEDULER ======
schedule.every(30).seconds.do(check_news)

print("Bot Running...")

while True:
    schedule.run_pending()
    time.sleep(1)
