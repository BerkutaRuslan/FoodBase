from rest_framework import generics
from rest_framework.permissions import AllowAny

from menu.models import Drink
from menu.serializers import DrinkSerializer


class ListAllDrinksView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = DrinkSerializer

    def get_queryset(self):
        drinks = Drink.objects.all()
        query_bottle_volume = self.request.GET.get("bottle_volume")
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if query_bottle_volume:
            drinks = drinks.filter(bottle_volume=query_bottle_volume)
        if min_price and max_price:
            drinks = drinks.filter(price__range=[min_price, max_price])
        return drinks

