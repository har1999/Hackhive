from django.urls import path
from django.contrib.auth import get_user_model
User = get_user_model()

from . import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupPageView.as_view(), name='signup'), 
    path('api/login/', views.DirectLoginView.as_view(), name='api-login'),
]
