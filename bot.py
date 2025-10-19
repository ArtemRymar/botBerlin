import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot




# Bot toket : 8456862882:AAHTMsL02_GluBff0n72ayVrptKi7n5mLtw

URL = "https://service.berlin.de/terminvereinbarung/termin/taken/"
CHAT_IDS = [544553533, 597176487]
TOKEN = "8456862882:AAHTMsL02_GluBff0n72ayVrptKi7n5mLtw"

NO_APPOINTMENTS_TEXT = "Leider sind aktuell keine Termine für ihre Auswahl verfügbar."

bot = Bot(token = TOKEN)

async def check_appointments():

    found_no_slots = False

    try:

        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup)

        
        all_potential_headers = soup.find_all('h1', class_='title')

        
        for header in all_potential_headers:
            header_text = header.get_text(strip=True)
            if NO_APPOINTMENTS_TEXT in header_text:
                found_no_slots = True
                break

        if found_no_slots:
            # Текст "нет мест" найден.
            print("❌ Нет свободных мест. Уведомление об отсутствии найдено.")

        else:
            
            print("✅ ПОТЕНЦИАЛЬНО ЕСТЬ МЕСТА! Срочно проверяйте сайт!")
            message = "⚠️⚠️ **ПОЯВИЛИСЬ СВОБОДНЫЕ МЕСТА НА BERLIN-PORTAL!** Срочно проверьте! ⚠️⚠️\n\n" + URL
            
            # Предполагаем, что CHAT_ID теперь CHAT_IDS и используем цикл, как мы договорились
            for chat_id in CHAT_IDS: 
                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

        


    except requests.exceptions.HTTPError as e:
        
        print(f"❌ HTTP Ошибка при проверке сайта: {e}")
        
        for chat_id in CHAT_IDS:
             await bot.send_message(chat_id=chat_id, text=f"Бот столкнулся с ошибкой доступа (4xx/5xx): {e}")
             
    except Exception as e:
        
        print(f"❌ Неизвестная ошибка: {e}")
        for chat_id in CHAT_IDS:
             await bot.send_message(chat_id=chat_id, text=f"Бот столкнулся с неизвестной ошибкой: {e}")

async def main():
    counter = 0
    while True:
        await check_appointments()
        if counter % 17280 == 0: # every 24 hours if sleep is 5 sec
            for chat_id in CHAT_IDS:
                await bot.send_message(chat_id=chat_id, text="✅ Бот работает. Проверки выполняются.")

        counter += 1
        await asyncio.sleep(5) #every 10 seconds for testing
    

if __name__ == "__main__":
    # The standard way to run the async main function
    asyncio.run(main())