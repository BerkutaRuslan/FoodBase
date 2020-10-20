from rest_framework import generics
from rest_framework.permissions import AllowAny

from menu.models import Drink, Dish, MenuOfDay
from menu.serializers import DrinkSerializer, DishSerializer, MenuOfDaySerializer


class ListAllDrinksView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = DrinkSerializer

    def get_queryset(self):
        drinks = Drink.objects.all()
        query_bottle_volume = self.request.GET.get("bottle_volume")
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if query_bottle_volume:
            drinks = drinks.filter(bottle_volume=query_bottle_volume)
        if min_price and max_price:
            drinks = drinks.filter(price__range=[min_price, max_price])
        return drinks


class GetDrinkByIdView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DrinkSerializer
    queryset = Drink.objects.all()


class GetDishByIdView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DishSerializer
    queryset = Dish.objects.all()


class GetMenuOfDayMealView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MenuOfDaySerializer
    queryset = MenuOfDay.objects.all()


class ListAllDishesView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DishSerializer

    def get_queryset(self):
        dishes = Dish.objects.all()
        query_category = self.request.GET.get("category")
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        sort_min_max = self.request.GET.get('sort_min_max')
        sort_max_min = self.request.GET.get('sort_max_min')

        if query_category:
            dishes = dishes.filter(category=query_category)
        if min_price and max_price:
            dishes = dishes.filter(price__range=[min_price, max_price])
        if sort_min_max:
            dishes = dishes.order_by('price')
        if sort_max_min:
            dishes = dishes.order_by('-price')
        return dishes
