from django.db import models

# Модель столика в ресторане
class Table(models.Model):
    number = models.CharField(max_length=10) # Номер столика
    location = models.CharField(
        max_length=100, null=True, blank=True
    ) # Расположение столика

    def __str__(self):
        return f"Столик {self.number}" # Чтобы в админке и выводах отображался номер столика

# Модель доступного временного слота для столика
class TableAvailableSlot(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="available_slots"
    ) # Связь с конкретным столиком (при удалении столика удаляются и слоты)
    date = models.DateField() # Дата доступного слота
    time = models.TimeField() # Время доступного слота

    def __str__(self):
        return f"{self.table} - {self.date} {self.time}" # Отображение в формате: столик - дата время

# Модель бронирования столика
class TableReservation(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="reservations"
    )  # Выбор столика для брони
    name = models.CharField(max_length=100) # Имя клиента (обязательно)
    surname = models.CharField(max_length=100) # Фамилия клиента (обязательно)
    patronymic = models.CharField(
        max_length=100, null=True, blank=True
    ) # Отчество (необязательно)
    email = models.EmailField(null=True, blank=True) # Email (необязательно)
    phone = models.CharField(max_length=15) # Телефон (обязательно)
    date = models.DateField() # Дата брони (обязательно)
    time = models.TimeField() # Время брони (обязательно)
    guests_number = models.IntegerField() # Количество гостей (обязательно)
    description = models.TextField(null=True, blank=True) # Доп. информация (необязательно)
    agreed_to_policy = models.BooleanField(default=False) # Согласие с политикой (обязательно)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.date} {self.time}" # Отображение брони

# Модель обращений клиентов (предложения, жалобы, заявления)
class Tableappeal(models.Model):
    Appeal_type_choises = [
        ("Предложение", "Предложение"),
        ("Заявление", "Заявление"),
        ("Жалоба", "Жалоба"),
    ] # Виды обращений
    name_surname_patronymic = models.CharField(max_length=200) # Имя и фамилия клиента
    email = models.CharField(max_length=100) # Email клиента
    phone = models.CharField(max_length=15, null=True, blank=True) # Телефон (необязательно)
    appeal_type_select = models.CharField(
        max_length=20, choices=Appeal_type_choises, default="Предложение"
    ) # Тип обращения, выбирается из списка
    appeal_text = models.TextField() # Текст обращения
    agreed_to_policy1 = models.BooleanField(default=False) # Согласие с политикой

    def __str__(self) -> str:
        return self.name_surname_patronymic # Отображение имени клиента

# Модель напитков в ресторане
class TableDrink(models.Model):
    drink_type_choises = [
        ("champagne", "Шампанское и игристые вина"),
        ("beer", "Пиво"),
        ("strong_drinks", "Крепкие напитки"),
        ("cocktails", "Коктейли"),
        ("non_alcoholic", "Безалкагольные напитки"),
    ] # Категории напитков
    name = models.CharField(max_length=100) # Название напитка
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена напитка
    description_drink = models.TextField() # Описание напитка
    structure_drink = models.JSONField() # Состав напитка (хранится в формате JSON)
    image_drink = models.ImageField(upload_to="drink_images/") # Фото напитка
    drink_type_select = models.CharField(
        max_length=50, choices=drink_type_choises, default="champange"
    ) # Выбор категории напитка

    def __str__(self):
        return self.name # Отображение названия напитка

# Модель оценки пользователями (например, еды и сервиса)
class UserRating(models.Model):
    food_rating = models.IntegerField()  # Оценка еды (1-5)
    service_rating = models.IntegerField()  # Оценка обслуживания (1-5)
    atmosphere_rating = models.IntegerField(default=3) # Оценка атмосферы (по умолчанию 3)
    created_at = models.DateTimeField(auto_now_add=True) # Время создания оценки (ставится автоматически)

    def __str__(self):
        return f"Food: {self.food_rating}, Service: {self.service_rating}" # Отображение оценки




"""
Рекомендательная система для сайта ресторана
Пример:
У пользователя есть параметры:
"Насколько голоден?" (мало, средне, очень).
"Предпочтение по кухне?" (европейская, азиатская, микс).
"Бюджет?" (низкий, средний, высокий).
Система на основе нечеткой логики определяет, какие блюда предложить.
Реализация:

Используйте правила вида:
Если "голоден сильно" и "бюджет высокий", то предлагать "стейки и основное блюдо".
Если "голоден слабо" и "бюджет низкий", то предлагать "салаты или супы".





Интерактивный чат-бот для поддержки клиентов
Внедрите чат-бота, использующего нечеткую логику для понимания запросов пользователей и предоставления релевантных ответов:

Входные данные: Вопросы и запросы пользователей.
Нечеткие правила: Интерпретация намерений пользователей, даже если запросы сформулированы нечетко или неоднозначно.
Выходные данные: Соответствующие ответы, рекомендации по меню, информация о бронировании и т.д.


javascript - которая работает по системе оценки
система оценкивания добавить на сайт
"""
