from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from menu.models import Drink, Dish, MenuOfDay, Cart
from menu.serializers import DrinkSerializer, DishSerializer, MenuOfDaySerializer, CartAddSerializer


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


class CardAddView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartAddSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data.pop('product_id'), serializer.validated_data.pop('product_type')
            quantity = serializer.validated_data.pop('quantity')
            product = serializer.save()
            cart, _ = Cart.objects.get_or_create(user=request.user, product=product, quantity=quantity)
            return Response({'message': 'Product was added to your cart!'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
