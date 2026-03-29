from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.worker_job_feed, name='worker_feed'),
    path('my-jobs/', views.worker_my_jobs, name='worker_my_jobs'),
    path('profile/<int:user_id>/', views.worker_profile_view, name='honest_profile'),
    path('apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
    path('complete/<int:engagement_id>/', views.mark_job_complete, name='mark_job_complete'),
]