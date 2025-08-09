from datetime import datetime, timedelta, time
from django.utils import timezone
from .models import Table, TableAvailableSlot

def populate_slots():
    tables = Table.objects.all() # Получаем все столики из базы
    start_date = timezone.now().date() # Текущая дата (сегодня)
    end_date = start_date + timedelta(days=15) # Конечная дата — через 15 дней от сегодня
    working_hours = [time(hour, 0) for hour in range(12, 22)] # Время работы с 12:00 до 21:00 (по часам)

    for table in tables: # Для каждого столика
        current_date = start_date # Начинаем с сегодняшнего дня
        while current_date <= end_date: # Пока не достигнем даты через 15 дней
            for slot_time in working_hours: # Для каждого рабочего часа
                # Проверяем, есть ли уже слот с таким столиком, датой и временем
                if not TableAvailableSlot.objects.filter(
                    table=table, date=current_date, time=slot_time
                ).exists():
                    # Если слота нет — создаём новый доступный слот для бронирования
                    TableAvailableSlot.objects.create(
                        table=table,
                        date=current_date,
                        time=slot_time
                    )
            current_date += timedelta(days=1) # Переходим к следующему дню
    print("Слоты успешно заполнены!") # Выводим сообщение об успешном завершении
