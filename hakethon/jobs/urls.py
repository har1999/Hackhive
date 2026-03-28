from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_to_job, name='apply-job'),
    path('complete/<int:engagement_id>/', views.mark_job_complete, name='complete-job'),
]
