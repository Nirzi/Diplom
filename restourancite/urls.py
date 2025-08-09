from django.urls import path, include
from . import views  # импортируем наши представления
from .views import get_drink_by_id
from .views import get_available_dates_times, get_drink_count
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('TableReservation_view/', views.TableReservation_view, name='TableReservation_view'),
    path('Tableappeal_view/', views.Tableappeal_view, name='Tableappeal_view'),
    path('get-drink/<int:id>/', get_drink_by_id, name='get_drink_by_id'),
    path('drink/', views.drink, name="drink"),
    path('get_drink_count/', get_drink_count, name='get_drink_count'),
    path('get-available-dates-times/<int:table_id>/', get_available_dates_times, name='get_available_dates_times'),
    path('calculate_overall_rating/', views.calculate_overall_rating, name='calculate_overall_rating'),
    path('rate/', views.rate_page, name='rate'),
]
if settings.DEBUG:
    urlpatterns += static('/drink_images/', document_root=os.path.join(settings.BASE_DIR, 'drink_images'))
