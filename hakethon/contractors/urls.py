from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='contractor_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('job/<int:job_id>/close/', views.close_job, name='close_job'),
    path('hire/<int:application_id>/', views.hire_worker, name='hire_worker'),
    path('rate/<int:engagement_id>/', views.rate_worker, name='rate_worker'),
    path('favourite/<int:worker_id>/', views.toggle_favourite, name='toggle_favourite'),
]