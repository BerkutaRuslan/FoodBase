from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News
from news.serializers import NewsSerializer


class GetAllNewsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class GetSingleNewsView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class GetRandomNewsView(APIView):
    def get(self, request):
        random_news = News.objects.order_by('?').first()
        return Response({"id": random_news.id,
                         "title": random_news.title,
                         "description": random_news.description,
                         "creation_date": random_news.creation_date.isoformat(' ', 'seconds'),
                         "photo": f'/media/{random_news.photo}'}, status=status.HTTP_200_OK)
