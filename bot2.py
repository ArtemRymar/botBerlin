import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Твой токен и chat_id (user_id)
TOKEN = "8104546885:AAGI4mGtG2xKi-GsKoHjxKRI7DZ4QDR60Ks"
CHAT_ID = 544553533

# Ссылка на страницу общежитий
URL = "https://www.stwdo.de/en/living-houses-application/current-housing-offers#residential-offer-list"



# создаём объект бота
bot = Bot(token=TOKEN)

async def check_offers():
    """
    Проверяет сайт на наличие предложений.
    Если они есть — шлёт сообщение в Telegram.
    """
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # ищем блок с уведомлением No results
        offers = soup.find_all("div", class_="listing")
        header = soup.find("header", class_="notification__header")

        if header:
            text = header.get_text(strip=True)
            if text == "No results":
                print("Нет предложений.")
            else:
                print("Есть предложения!")
                await bot.send_message(chat_id=CHAT_ID, text="⚠️ Появились предложения в общежитии! Проверь сайт!")
        else:
            print("Есть предложения (блок отсутствует)!")
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ Появились предложения в общежитии! Проверь сайт!")

        if offers:
            print("Найдено объявлений:")
            await bot.send_message(chat_id=CHAT_ID, text="Найдено объявлений:")
            

    except Exception as e:
        print(f"Ошибка при проверке сайта: {e}")
        await bot.send_message(chat_id=CHAT_ID, text=f"Бот столкнулся с ошибкой: {e}")

async def main():
    counter = 0
    while True:
        await check_offers()
        if counter % 12 == 0:
            await bot.send_message(chat_id=CHAT_ID, text="✅ Бот работает. Проверки выполняются.")

        counter += 1
        await asyncio.sleep(300)   # каждые 5 минут

if __name__ == "__main__":
    asyncio.run(main())