from rest_framework import serializers

from news.models import News


class AllNewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'creation_date', 'photo']
