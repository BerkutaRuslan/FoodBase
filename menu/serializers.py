from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from menu.models import Drink, Dish, MenuOfDay, Product


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


class CartAddSerializer(serializers.Serializer):
    product_type = serializers.CharField(required=True)
    product_id = serializers.CharField(required=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def validate(self, attrs):
        product_type, product_id = attrs['product_type'], attrs['product_id']
        try:
            if product_type == 'drink':
                drink = Drink.objects.get(id=product_id)
                if drink:
                    attrs['name'] = drink.name
                    attrs['image'] = drink.photo
                    attrs['price'] = drink.price
                    return attrs
            elif product_type == 'dish':
                dish = Dish.objects.get(id=product_id)
                if dish:
                    attrs['name'] = dish.name
                    attrs['image'] = dish.photo
                    attrs['price'] = dish.price
                    return attrs
        except Drink.DoesNotExist:
            msg = "Unfortunately, we don't have that product in our menu"
            raise ValidationError(msg)

