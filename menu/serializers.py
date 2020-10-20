from rest_framework import serializers

from menu.models import Drink, Dish, MenuOfDay


class DrinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drink
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = '__all__'


class MenuOfDaySerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=False, read_only=True)
    drink = DrinkSerializer(many=False, read_only=True)

    class Meta:
        model = MenuOfDay
        fields = ['dish', 'drink', 'price', 'expire']
