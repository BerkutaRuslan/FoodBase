from django.urls import path

from menu.views import ListAllDrinksView, GetDrinkByIdView, GetDishByIdView, GetMenuOfDayMealView, ListAllDishesView, \
    CardAddView

urlpatterns = [
    path('drinks', ListAllDrinksView.as_view(), name='drinks'),
    path('dishes', ListAllDishesView.as_view(), name='dishes'),
    path('drinks/<int:pk>', GetDrinkByIdView.as_view()),
    path('dish/<int:pk>', GetDishByIdView.as_view()),
    path('special-proposition', GetMenuOfDayMealView.as_view()),
    path('cart/add/', CardAddView.as_view(), name='cart_add'),
]
