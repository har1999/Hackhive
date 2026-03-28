from django.urls import path
from jobs import views as job_views
from . import views

urlpatterns = [
    path('feed/', job_views.worker_job_feed, name='worker-feed'),
    path('my-jobs/', job_views.worker_my_jobs, name='worker-my-jobs'),
    path('profile/', job_views.worker_profile_view, name='worker-profile'),
    path('profile/<int:user_id>/', job_views.worker_profile_view, name='worker-profile-detail'),
    path('setup/', views.worker_setup, name='worker-setup'),
]
