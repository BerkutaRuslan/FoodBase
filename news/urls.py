from django.urls import path

from news.views import *

urlpatterns = [
    path('', GetAllNewsView.as_view()),
    path('<int:pk>', GetSingleNewsView.as_view()),
    path('random', GetRandomNewsView.as_view()),
]
