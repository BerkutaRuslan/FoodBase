from django.urls import path

from menu.views import ListAllDrinksView

urlpatterns = [
    path('drinks', ListAllDrinksView.as_view())
]
