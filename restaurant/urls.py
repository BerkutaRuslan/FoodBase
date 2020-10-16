from django.urls import path

from restaurant.views import RestaurantHomePageView, RestaurantPlaceInformation

urlpatterns = [
    path('', RestaurantHomePageView.as_view()),
    path('address', RestaurantPlaceInformation.as_view()),
]
