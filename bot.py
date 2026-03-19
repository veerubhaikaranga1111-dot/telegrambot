import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

BOT_TOKEN = "8337254899:AAGcUk0FN7BDDM6GUgupuDJzd55f8OKTpxE"
CHAT_ID = "1467665974"

bot = Bot(token=BOT_TOKEN)

sent_news = set()

def check_news():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr", class_="calendar__row")

    for row in rows:
        try:
            impact = row.find("td", class_="calendar__impact").get("title")
            currency = row.find("td", class_="calendar__currency").text.strip()
            event = row.find("td", class_="calendar__event").text.strip()
            time_news = row.find("td", class_="calendar__time").text.strip()

            unique_id = event + time_news

            # FILTER: Only high impact USD news
            if impact == "High Impact Expected" and currency == "USD":

                if unique_id not in sent_news:
                    sent_news.add(unique_id)

                    message = f"""
🚨 HIGH IMPACT USD NEWS 🚨

Event: {event}
Time: {time_news}

🔥 Affects:
XAUUSD (Gold)
BTCUSD / ETHUSD

PLAN:
Wait for liquidity sweep
Enter after displacement (SMC)
"""

                    bot.send_message(chat_id=CHAT_ID, text=message)

        except:
            continue


while True:
    check_news()
    time.sleep(30)  # every 30 seconds
