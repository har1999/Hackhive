from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='contractor-dashboard'),
    path('post-job/', views.post_job, name='post-job'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job-applicants'),
    path('hire/<int:application_id>/', views.hire_worker, name='hire-worker'),
    path('favourite/<int:worker_id>/', views.toggle_favourite, name='toggle-favourite'),
]
from ratings import views as rating_views
urlpatterns += [
    path('endorse/<int:engagement_id>/', rating_views.submit_endorsement, name='contractor-endorse'),
]
