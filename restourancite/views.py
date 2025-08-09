from django.shortcuts import render
from datetime import datetime, date, time
import requests
import html
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import TableDrink
from .models import Table, TableAvailableSlot
import numpy as np
import skfuzzy as fuzz
from .models import UserRating
from django.db.models import Q
from .telegram_bot import send_telegram_message


def rate_page(request):
    return render(request, "restourancite/rating.html")


def home(request):
    tables = Table.objects.filter(available_slots__isnull=False).distinct()
    return render(
        request, "restourancite/restourant_main_page.html", {"tables": tables}
    )


def menu(request):
    return render(request, "restourancite/restourant_menu.html")


def about(request):
    return render(request, "restourancite/restourant_me.html")


def contact(request):
    return render(request, "restourancite/restourant_contact.html")


def drink(request):
    return render(request, "restourancite/restourant_drink.html")


from django.shortcuts import render, redirect
from .models import TableReservation  # Импортируем модель


def get_drink_count(request):
    count = TableDrink.objects.count()
    return JsonResponse({"count": count})


def get_available_dates_times(request, table_id):
    """
    Возвращает доступные даты и время для данного столика,
    отфильтровывая прошедшие даты и время относительно текущего времени сервера.
    """
    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        return JsonResponse({'error': 'Столик не найден'}, status=404)

    # Получаем текущую дату и время
    today = date.today()
    now_time = datetime.now().time() # Используем datetime.now().time() для получения текущего времени

    # Фильтруем доступные слоты:
    # 1. Даты строго в будущем (больше текущей даты)
    # 2. Если дата сегодняшняя, то только время, которое больше или равно текущему времени
    available_slots = TableAvailableSlot.objects.filter(
        Q(table=table) &
        (
            Q(date__gt=today) |  # Даты после сегодняшней
            Q(date=today, time__gte=now_time) # Сегодняшняя дата, но время должно быть текущим или будущим
        )
    ).order_by('date', 'time') # Сортируем для последовательного отображения

    available_dates_times = {}
    for slot in available_slots:
        date_str = slot.date.strftime('%Y-%m-%d')
        time_str = slot.time.strftime('%H:%M')
        if date_str not in available_dates_times:
            available_dates_times[date_str] = []
        available_dates_times[date_str].append(time_str)

    return JsonResponse({'available_dates_times': available_dates_times})


def TableReservation_view(request):
    tables = Table.objects.filter(available_slots__isnull=False).distinct()
    if request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("form_name")
        surname = request.POST.get("form_surname")
        patronymic = request.POST.get("form_patronymic")
        email = request.POST.get("form_mail")
        phone = request.POST.get("form_telephone")
        date = request.POST.get("form_date")
        time = request.POST.get("form_time")
        guests_number = request.POST.get("form_number_guest")
        description = request.POST.get("floatingTextarea")
        agreed_to_policy = request.POST.get("flexCheckDefault")

        # Проверка обязательного согласия с политикой конфиденциальности
        if not agreed_to_policy:
            return render(
                request,
                "restourancite/restourant_main_page.html",
                {
                    "error": "Вы должны согласиться с политикой конфиденциальности для отправки формы.",
                    "tables": tables,
                },
            )

        # Проверка выбранного столика
        table_id = request.POST.get("form_table")
        if not table_id:
            return render(
                request,
                "restourancite/restourant_main_page.html",
                {"error": "Выберите столик.", "tables": tables},
            )
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return render(
                request,
                "restourancite/restourant_main_page.html",
                {"error": "Выбранный столик не существует.", "tables": tables},
            )

        # Проверка даты и времени
        if not date or not time:
            return render(
                request,
                "restourancite/restourant_main_page.html",
                {"error": "Выберите дату и время.", "tables": tables},
            )

        try:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()
            selected_time = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            return render(
                request,
                "restourancite/restourant_main_page.html",
                {"error": "Некорректный формат даты или времени.", "tables": tables},
            )

        # Проверяем, что слот доступен в TableAvailableSlot
        slot_exists = TableAvailableSlot.objects.filter(
            table=table, date=selected_date, time=selected_time
        ).exists()

        if not slot_exists:
            return render(
                request,
                "restourancite/restourant_main_page.html",
                {"error": "Выбранный слот недоступен.", "tables": tables},
            )

        # Проверка количества гостей
        try:
            guests_number = int(guests_number)
            if guests_number <= 0:
                return render(
                    request,
                    "restourancite/restourant_main_page.html",
                    {
                        "error": "Количество гостей должно быть больше нуля.",
                        "tables": tables,
                    },
                )
        except (ValueError, TypeError):
            return render(
                request,
                "restourancite/restourant_main_page.html",
                {"error": "Введите корректное количество гостей.", "tables": tables},
            )

        # Сохраняем данные в базу данных
        reservation = TableReservation(
            table=table,
            name=name,
            surname=surname,
            patronymic=patronymic,
            email=email,
            phone=phone,
            date=selected_date,
            time=selected_time,
            guests_number=guests_number,
            description=description,
            agreed_to_policy=True,
        )
        reservation.save()

        safe_table_number = html.escape(str(table.number))
        safe_name = html.escape(name)
        safe_surname = html.escape(surname)
        safe_phone = html.escape(phone)
        safe_email = html.escape(email or 'не указан')
        safe_guests = html.escape(str(guests_number))
        safe_description = html.escape(description or 'нет')

        # Формируем сообщение с безопасными данными
        message_text = (
            f"<b>🛎️ Новое бронирование столика!</b>\n\n"
            f"<b>Столик:</b> №{safe_table_number}\n"
            f"<b>Дата:</b> {selected_date.strftime('%d.%m.%Y')}\n"
            f"<b>Время:</b> {selected_time.strftime('%H:%M')}\n"
            f"<b>Имя:</b> {safe_name} {safe_surname}\n"
            f"<b>Телефон:</b> {safe_phone}\n"
            f"<b>Email:</b> {safe_email}\n"
            f"<b>Кол-во гостей:</b> {safe_guests}\n"
            f"<b>Описание:</b> {safe_description}"
        )
        
        # Отправляем сообщение
        send_telegram_message(message_text)
        
        # Удаляем слот из TableAvailableSlot
        TableAvailableSlot.objects.filter(
            table=table, date=selected_date, time=selected_time
        ).delete()

        # Обновляем список столиков с доступными слотами
        tables = Table.objects.filter(available_slots__isnull=False).distinct()

        # Вернуть сообщение об успехе на той же странице
        return render(
            request,
            "restourancite/restourant_main_page.html",
            {"success": "Ваше бронирование успешно сохранено!", "tables": tables},
        )

    return render(
        request, "restourancite/restourant_main_page.html", {"tables": tables}
    )


from .models import Tableappeal


def Tableappeal_view(request):
    if request.method == "POST":
        name_surname_patronymic = request.POST.get("form_FCs_appeal")
        email = request.POST.get("form_mail_appeal")
        appeal_type_select = request.POST.get("form_select_appeal")
        phone = request.POST.get("form_telephone_appeal")
        appeal_text = request.POST.get("floatingTextarea_appeal")
        agreed_to_policy1 = request.POST.get(
            "flexCheckDefault_appeal"
        )  # Это будет "true", если выбрано

        if not agreed_to_policy1:  # Проверка согласия с политикой
            return render(
                request,
                "restourancite/restourant_me.html",
                {
                    "error": "Вы должны согласиться с политикой конфиденциальности для отправки формы.",
                },
            )

        # Создаем и сохраняем новую запись
        appeal = Tableappeal(
            name_surname_patronymic=name_surname_patronymic,
            email=email,
            appeal_type_select=appeal_type_select,
            phone=phone,
            appeal_text=appeal_text,
            agreed_to_policy1=True,
        )
        appeal.save()
        
        message_text = (
            f"<b>🗣️ Новое обращение с сайта!</b>\n\n"
            f"<b>Тип:</b> {appeal_type_select}\n"
            f"<b>ФИО:</b> {name_surname_patronymic}\n"
            f"<b>Телефон:</b> {phone or 'не указан'}\n"
            f"<b>Email:</b> {email}\n\n"
            f"<b>Текст обращения:</b>\n{appeal_text}"
        )
        # Отправляем сообщение
        send_telegram_message(message_text)
        
        return render(
            request,
            "restourancite/restourant_me.html",
            {"success": "Ваше обращение успешно отправлено!"},
        )

    return render(request, "restourancite/restourant_me.html")


def get_drink_by_id(request, id):
    try:
        drink = TableDrink.objects.get(id=id)
        image_url = (
            request.build_absolute_uri(
                "/drink_images/" + drink.image_drink.name.split("/")[-1]
            )
            if drink.image_drink
            else None
        )
        data = {
            "name": drink.name,
            "price": drink.price,
            "description_drink": drink.description_drink,
            "structure_drink": drink.structure_drink,
            "image_drink": image_url,
            "drink_type_select": drink.drink_type_select,
        }
        return JsonResponse(data)
    except TableDrink.DoesNotExist:
        return JsonResponse({"error": "Drink not found"}, status=404)


def calculate_overall_rating(request):
    if request.method == "POST":
        try:
            # Получаем данные из формы
            food_rating = request.POST.get("food_rating")
            service_rating = request.POST.get("service_rating")
            atmosphere_rating = request.POST.get("atmosphere_rating")

            # Проверяем, что данные были переданы
            if not food_rating or not service_rating or not atmosphere_rating:
                return JsonResponse({"error": "Все оценки должны быть заполнены."}, status=400)

            # Преобразуем оценки в целые числа
            food_rating = int(food_rating)
            service_rating = int(service_rating)
            atmosphere_rating = int(atmosphere_rating)

            # Проверяем, что оценки находятся в допустимом диапазоне
            if not (1 <= food_rating <= 5) or not (1 <= service_rating <= 5) or not (1 <= atmosphere_rating <= 5):
                return JsonResponse({"error": "Оценки должны быть в диапазоне от 1 до 5"}, status=400)

            # Нечеткие множества
            x_food = np.arange(1, 6, 1)
            x_service = np.arange(1, 6, 1)
            x_atmosphere = np.arange(1, 6, 1)
            x_overall = np.arange(1, 6, 1)

            # Функции принадлежности для еды
            food_low = fuzz.trapmf(x_food, [1, 1, 2, 3])
            food_medium = fuzz.trimf(x_food, [2, 3, 4])
            food_high = fuzz.trapmf(x_food, [3, 4, 5, 5])

            # Функции принадлежности для обслуживания
            service_low = fuzz.trapmf(x_service, [1, 1, 2, 3])
            service_medium = fuzz.trimf(x_service, [2, 3, 4])
            service_high = fuzz.trapmf(x_service, [3, 4, 5, 5])

            # Функции принадлежности для атмосферы
            atmosphere_low = fuzz.trapmf(x_atmosphere, [1, 1, 2, 3])
            atmosphere_medium = fuzz.trimf(x_atmosphere, [2, 3, 4])
            atmosphere_high = fuzz.trapmf(x_atmosphere, [3, 4, 5, 5])

            # Функции принадлежности для итоговой оценки
            overall_low = fuzz.trapmf(x_overall, [1, 1, 2, 3])
            overall_medium = fuzz.trimf(x_overall, [2, 3, 4])
            overall_high = fuzz.trapmf(x_overall, [3, 4, 5, 5])

            # Вычисление степеней принадлежности для входных данных
            food_levels = {
                "low": fuzz.interp_membership(x_food, food_low, food_rating),
                "medium": fuzz.interp_membership(x_food, food_medium, food_rating),
                "high": fuzz.interp_membership(x_food, food_high, food_rating),
            }

            service_levels = {
                "low": fuzz.interp_membership(x_service, service_low, service_rating),
                "medium": fuzz.interp_membership(x_service, service_medium, service_rating),
                "high": fuzz.interp_membership(x_service, service_high, service_rating),
            }

            atmosphere_levels = {
                "low": fuzz.interp_membership(x_atmosphere, atmosphere_low, atmosphere_rating),
                "medium": fuzz.interp_membership(x_atmosphere, atmosphere_medium, atmosphere_rating),
                "high": fuzz.interp_membership(x_atmosphere, atmosphere_high, atmosphere_rating),
            }

            # Генерация правил (27 правил для 3 параметров)
            aggregated = np.zeros_like(x_overall)
            for food_level_name, food_level_value in food_levels.items():
                for service_level_name, service_level_value in service_levels.items():
                    for atmosphere_level_name, atmosphere_level_value in atmosphere_levels.items():
                        rule_strength = min(
                            food_level_value, service_level_value, atmosphere_level_value
                        )

                        # Определяем уровень итоговой оценки
                        if food_level_name == "low" and service_level_name == "low" and atmosphere_level_name == "low":
                            aggregated = np.fmax(aggregated, rule_strength * overall_low)
                        elif food_level_name == "high" and service_level_name == "high" and atmosphere_level_name == "high":
                            aggregated = np.fmax(aggregated, rule_strength * overall_high)
                        else:
                            aggregated = np.fmax(aggregated, rule_strength * overall_medium)

            # Дефаззификация
            overall_score = fuzz.defuzz(x_overall, aggregated, "centroid")

            # Сохранение данных в базу
            UserRating.objects.create(
                food_rating=food_rating,
                service_rating=service_rating,
                atmosphere_rating=atmosphere_rating,
            )

            # Возврат результата
            return JsonResponse({"overall_score": round(overall_score, 2)})

        except Exception as e:
            return JsonResponse({"error": f"Ошибка расчёта: {str(e)}"}, status=500)

    return JsonResponse({"error": "Метод запроса должен быть POST"}, status=400)