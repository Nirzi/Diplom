from django.contrib import admin

from .models import TableReservation, Tableappeal, TableDrink,TableAvailableSlot,Table

admin.site.register(TableReservation)
admin.site.register(Tableappeal)
admin.site.register(TableDrink)
admin.site.register(Table)
admin.site.register(TableAvailableSlot)

