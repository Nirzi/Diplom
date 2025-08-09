# restourancite/telegram_bot.py

import requests
from django.conf import settings

def send_telegram_message(message: str):
    """
    Отправляет сообщение в Telegram чат, используя токен и ID из settings.py.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # URL для запроса к Telegram API
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    # Параметры запроса
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML' # Используем HTML для форматирования текста (жирный, курсив)
    }
    
    try:
        # Отправляем запрос
        response = requests.get(url, params=params)
        response.raise_for_status() # Проверяем, что запрос прошел успешно
        print("Telegram message sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        # В случае ошибки выводим ее в консоль
        print(f"Failed to send Telegram message: {e}")
        return False