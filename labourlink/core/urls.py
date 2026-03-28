from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('worker/', views.worker_profile, name='worker_profile'),
    path('jobs/', views.job_board, name='job_board'),
    path('contractor/dashboard/', views.contractor_dashboard, name='contractor_dashboard'),
    path('voice/', views.voice_ui, name='voice_ui'),
]
