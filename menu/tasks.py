from celery import shared_task
import random

from menu.models import MenuOfDay, Dish, Drink


@shared_task
def create_menu_of_day():
    MenuOfDay.objects.all().delete()
    random_dish, random_drink = Dish.objects.order_by('?')[0], Drink.objects.order_by('?')[0]

    dish_price, drink_price = random_dish.price, random_drink.price
    new_price = (dish_price + drink_price) - (dish_price + drink_price) / 100 * 20
    MenuOfDay.objects.create(dish_id=random_dish.id, drink_id=random_drink.id,
                             price=float("{:.2f}".format(new_price)))
    return f'New menu of the day was created! '
