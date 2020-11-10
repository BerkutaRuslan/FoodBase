from datetime import datetime, timedelta

from django.db import models

from FoodBase import settings
from accounts.models import User


def get_expire_date():
    return datetime.today() + timedelta(days=1)


category_choice = (
    ('pizza', 'pizza'),
    ('burger', 'burger'),
    ('sushi', 'sushi'),
    ('first meal', 'first meal'),
    ('second meal', 'second meal'),
    ('dessert', 'dessert'),
)

product_type_choice = (
    ('drink', 'drink'),
    ('dish', 'dish'),
)

volume_choice = (
    ('0.5', '0.5',),
    ('1', '1'),
    ('1.5', '1.5'),
    ('2', '2'),
)


class Dish(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    price = models.FloatField()
    calories = models.IntegerField()
    weight = models.FloatField()
    category = models.CharField(choices=category_choice, max_length=100)
    photo = models.ImageField(upload_to='dish', default=settings.DISH_DEFAULT_IMAGE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Dish'


class Drink(models.Model):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='drinks', default=settings.DRINK_DEFAULT_IMAGE)
    bottle_volume = models.CharField(max_length=150, choices=volume_choice)
    price = models.FloatField()

    def __str__(self):
        return self.name


class MenuOfDay(models.Model):
    expire = models.DateField(default=get_expire_date)
    price = models.FloatField()
    dish = models.ForeignKey(Dish, related_name='DayDish', on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, related_name='Drink', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dish.name) + ', ' + str(self.drink.name) + ', ' + str(self.price)

    class Meta:
        verbose_name_plural = 'Menu of day'


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    price = models.FloatField()

    def __str__(self):
        return str(self.name) + ', ' + str(self.price)
