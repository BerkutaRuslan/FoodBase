from django.urls import path

from accounts.views import SignInRequestView

urlpatterns = [
    path('sign-in-request', SignInRequestView.as_view())
]