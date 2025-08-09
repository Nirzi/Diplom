import requests
from django.conf import settings

def send_telegram_message(message: str):
    """
    Функция для отправки сообщения в Telegram чат.
    Использует токен бота и ID чата, которые хранятся в settings.py.
    """
    # Получаем токен Telegram-бота и идентификатор чата из настроек проекта
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # Формируем URL для API Telegram.
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    # Параметры запроса, которые передаются в Telegram API
    params = {
        'chat_id': chat_id, # Куда отправить сообщение (ID чата)
        'text': message, # Текст сообщения, который мы хотим отправить
        'parse_mode': 'HTML' # Форматирование текста
    }
    
    try:
        # Выполняем GET-запрос к API Telegram с указанными параметрами
        response = requests.get(url, params=params)
        # Проверяем статус ответа — если код ошибки (например 400 или 500), будет исключение
        response.raise_for_status()
        # Если всё прошло успешно, выводим сообщение в консоль
        print("Telegram message sent successfully!")
        return True # Возвращаем True — сообщение отправлено успешно
    except requests.exceptions.RequestException as e:
        # Если произошла ошибка при запросе, ловим исключение и выводим текст ошибки
        print(f"Failed to send Telegram message: {e}")
        return False # Возвращаем False — сообщение отправить не удалось