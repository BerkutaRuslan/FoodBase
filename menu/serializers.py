from rest_framework import serializers

from menu.models import Drink


class DrinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drink
        fields = '__all__'

