from django.contrib import admin

from FoodBase.menu.models import Dish, MenuOfDay, Drink

admin.site.register(Dish)
admin.site.register(Drink)
admin.site.register(MenuOfDay)
