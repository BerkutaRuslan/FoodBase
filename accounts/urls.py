from django.urls import path

from accounts.views import SignInRequestView, SignInVerifyView, UserProfileView

urlpatterns = [
    path('sign-in-request', SignInRequestView.as_view()),
    path('sign-in-verify', SignInVerifyView.as_view()),
    path('profile', UserProfileView.as_view()),
]