from django.urls import path, include
from . import views  # импортируем наши представления
from .views import get_drink_by_id
from .views import get_available_dates_times, get_drink_count
from django.conf import settings
from django.conf.urls.static import static
import os

# Создаем список URL-шаблонов (роутов), которые будут обрабатываться нашим приложением
urlpatterns = [
    # Главная страница сайта — пустой путь '' значит корень сайта
    path('', views.home, name='home'),
    # Страница с меню ресторана
    path('menu/', views.menu, name='menu'),
    # Страница "О нас"
    path('about/', views.about, name='about'),
    # Контакты
    path('contact/', views.contact, name='contact'),
    # Страница бронирования столиков
    path('TableReservation_view/', views.TableReservation_view, name='TableReservation_view'),
    # Страница подачи обращений (жалобы, предложения и т.п.)
    path('Tableappeal_view/', views.Tableappeal_view, name='Tableappeal_view'),
    # Получить данные напитка по его ID (параметр передается в URL)
    path('get-drink/<int:id>/', get_drink_by_id, name='get_drink_by_id'),
    # Страница с напитками
    path('drink/', views.drink, name="drink"),
    # Получить количество напитков (возможно для динамического обновления на сайте)
    path('get_drink_count/', get_drink_count, name='get_drink_count'), 
    # Получить доступные даты и время для бронирования конкретного столика (table_id — параметр URL)
    path('get-available-dates-times/<int:table_id>/', get_available_dates_times, name='get_available_dates_times'),
    # Рассчитать общую оценку (например, рейтинги ресторана)
    path('calculate_overall_rating/', views.calculate_overall_rating, name='calculate_overall_rating'),
    # Страница для выставления оценки (рейтинга)
    path('rate/', views.rate_page, name='rate'),
]
# Если мы в режиме отладки
if settings.DEBUG:
    # Добавляем возможность отдачи статических файлов (например, картинок напитков)
    urlpatterns += static('/drink_images/', document_root=os.path.join(settings.BASE_DIR, 'drink_images'))
