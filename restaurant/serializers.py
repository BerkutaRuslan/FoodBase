from rest_framework import serializers

from restaurant.models import Restaurant


class FindUsSerailizer(serializers.ModelSerializer):
    class Meta:
        Model = Restaurant
        fields = ['work_from', 'work_to', 'latitude', 'longitude']
