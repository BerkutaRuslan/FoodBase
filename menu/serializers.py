from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from menu.models import Drink, Dish, MenuOfDay, Product, Cart


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
    quantity = serializers.CharField(required=True)

    def create(self, validated_data):
        product, created = Product.objects.get_or_create(**validated_data)
        return product

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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['product', 'quantity', 'total_amount']

    def get_total_amount(self, obj):
        total_amount = 0
        product_quantity = obj.quantity
        total_amount = total_amount + obj.product.price * product_quantity
        return total_amount


class UpdateCartSerializer(serializers.Serializer):
    quantity = serializers.CharField(required=True)
    product_id = serializers.CharField(required=True)

    def validate(self, attrs):
        quantity = attrs['quantity']
        product_id = attrs['product_id']
        if int(quantity) >= 1:
            if Cart.objects.get(user=self.instance, product_id=product_id):
                return attrs
            else:
                msg = "Product with that id does not exists"
                return ValidationError(msg)
        else:
            msg = "Quantity can be 1 or greater"
            return ValidationError(msg)
