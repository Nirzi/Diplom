from django.apps import AppConfig

class RestouranciteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restourancite'

    def ready(self):
        from .populate_slots import populate_slots  # Убедись, что путь правильный
        populate_slots()  # Вызов функции при запуске приложения
