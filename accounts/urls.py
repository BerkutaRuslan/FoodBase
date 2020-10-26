from django.urls import path

from accounts.views import SignInRequestView, SignInVerifyView

urlpatterns = [
    path('sign-in-request', SignInRequestView.as_view()),
    path('sign-in-verify', SignInVerifyView.as_view()),
]