from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News
from news.serializers import AllNewsSerializer


class GetAllNewsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = AllNewsSerializer


