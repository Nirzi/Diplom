from django.db import models


class Table(models.Model):
    number = models.CharField(max_length=10)  # Номер столика
    location = models.CharField(
        max_length=100, null=True, blank=True
    )

    def __str__(self):
        return f"Столик {self.number}"


class TableAvailableSlot(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="available_slots"
    )
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.table} - {self.date} {self.time}"


class TableReservation(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="reservations"
    )  # Добавляем выбор столика
    name = models.CharField(max_length=100)  # Обязательное поле
    surname = models.CharField(max_length=100)  # Обязательное поле
    patronymic = models.CharField(
        max_length=100, null=True, blank=True
    )  # Необязательное поле
    email = models.EmailField(null=True, blank=True)  # Необязательное поле
    phone = models.CharField(max_length=15)  # Обязательное поле
    date = models.DateField()  # Обязательное поле
    time = models.TimeField()  # Обязательное поле
    guests_number = models.IntegerField()  # Обязательное поле
    description = models.TextField(null=True, blank=True)  # Необязательное поле
    agreed_to_policy = models.BooleanField(default=False)  # Обязательное поле

    def __str__(self):
        return f"{self.name} {self.surname} - {self.date} {self.time}"


class Tableappeal(models.Model):
    Appeal_type_choises = [
        ("Предложение", "Предложение"),
        ("Заявление", "Заявление"),
        ("Жалоба", "Жалоба"),
    ]
    name_surname_patronymic = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    appeal_type_select = models.CharField(
        max_length=20, choices=Appeal_type_choises, default="Предложение"
    )
    appeal_text = models.TextField()
    agreed_to_policy1 = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name_surname_patronymic


class TableDrink(models.Model):
    drink_type_choises = [
        ("champagne", "Шампанское и игристые вина"),
        ("beer", "Пиво"),
        ("strong_drinks", "Крепкие напитки"),
        ("cocktails", "Коктейли"),
        ("non_alcoholic", "Безалкагольные напитки"),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description_drink = models.TextField()
    structure_drink = models.JSONField()
    image_drink = models.ImageField(upload_to="drink_images/")
    drink_type_select = models.CharField(
        max_length=50, choices=drink_type_choises, default="champange"
    )

    def __str__(self):
        return self.name
      
class UserRating(models.Model):
    food_rating = models.IntegerField()  # Оценка еды (1-5)
    service_rating = models.IntegerField()  # Оценка обслуживания (1-5)
    atmosphere_rating = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)  # Время оценки

    def __str__(self):
        return f"Food: {self.food_rating}, Service: {self.service_rating}"


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
