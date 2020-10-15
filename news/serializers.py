from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    creation_date = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'creation_date', 'photo']

    def get_creation_date(self, obj):
        date_without_microseconds = obj.creation_date.isoformat(' ', 'seconds')
        return date_without_microseconds
