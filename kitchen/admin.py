from django.contrib import admin

from kitchen.models import Cook, Dish, DishType, Ingredient

admin.site.register(DishType)
admin.site.register(Cook)
admin.site.register(Dish)
admin.site.register(Ingredient)
