from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api/request-otp/', views.RequestOTPView.as_view(), name='api-request-otp'),
    path('api/verify-otp/', views.VerifyOTPView.as_view(), name='api-verify-otp'),
]
