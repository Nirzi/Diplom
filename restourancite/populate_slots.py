
from datetime import datetime, timedelta, time
from django.utils import timezone
from .models import Table, TableAvailableSlot

def populate_slots():
    tables = Table.objects.all()
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=15)
    working_hours = [time(hour, 0) for hour in range(12, 22)]  # С 12:00 до 21:00

    for table in tables:
        current_date = start_date
        while current_date <= end_date:
            for slot_time in working_hours:
                if not TableAvailableSlot.objects.filter(
                    table=table, date=current_date, time=slot_time
                ).exists():
                    TableAvailableSlot.objects.create(
                        table=table,
                        date=current_date,
                        time=slot_time
                    )
            current_date += timedelta(days=1)
    print("Слоты успешно заполнены!")
