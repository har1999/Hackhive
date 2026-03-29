from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupPageView.as_view(), name='signup'),
    path('api/direct-login/', views.DirectLoginView.as_view(), name='api-direct-login'),
]