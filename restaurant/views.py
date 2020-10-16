from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.models import Restaurant
from restaurant.serializers import FindUsSerailizer
from restaurant.utils import get_restaur_info, restaurant_place_info


class RestaurantHomePageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Restaurant.objects.all()
        for restaurant in queryset:
            return Response(get_restaur_info(restaurant), status=status.HTTP_200_OK)


class RestaurantPlaceInformation(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Restaurant.objects.all()
        for restaurant in queryset:
            return Response(restaurant_place_info(restaurant), status=status.HTTP_200_OK)
