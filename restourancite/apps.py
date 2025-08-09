from django.apps import AppConfig

# Настройка приложения Django
class RestouranciteConfig(AppConfig):
    # Тип поля, который будет использоваться по умолчанию для ID в базах данных
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restourancite'

    # Этот метод запускается, когда приложение готово к работе
    def ready(self):
        # Импортируем функцию, которая заполняет какие-то данные (слоты для бронирования)
        from .populate_slots import populate_slots
        # Запускаем эту функцию, чтобы сразу при старте приложения создать нужные данные
        populate_slots()
