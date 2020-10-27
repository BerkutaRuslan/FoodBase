from django.urls import path

from accounts.views import SignInRequestView, SignInVerifyView, UserProfileView, UpdatePhotoView, ForgotPasswordView, \
    ResetPasswordView

urlpatterns = [
    path('sign-in-request', SignInRequestView.as_view()),
    path('sign-in-verify', SignInVerifyView.as_view()),
    path('profile', UserProfileView.as_view()),
    path('profile/photo', UpdatePhotoView.as_view()),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgotPassword'),
    path('reset-password', ResetPasswordView.as_view(), name='resetPassword'),
]