from django.urls import path

from menu.views import ListAllDrinksView, GetDrinkByIdView, GetDishByIdView, GetMenuOfDayMealView, ListAllDishesView

urlpatterns = [
    path('drinks', ListAllDrinksView.as_view()),
    path('dishes', ListAllDishesView.as_view()),
    path('drinks/<int:pk>', GetDrinkByIdView.as_view()),
    path('dish/<int:pk>', GetDishByIdView.as_view()),
    path('special-proposition', GetMenuOfDayMealView.as_view()),
]
