from rest_framework import generics
from rest_framework.permissions import AllowAny

from menu.models import Drink
from menu.serializers import DrinkSerializer


class ListAllDrinksView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = DrinkSerializer

    def get_queryset(self):
        query_bottle_volume = self.request.GET.get("bottle_volume")
        if query_bottle_volume:
            return Drink.objects.filter(bottle_volume=query_bottle_volume)
        else:
            return Drink.objects.all()
