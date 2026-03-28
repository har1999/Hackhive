from django.urls import path
from . import views

urlpatterns = [
    path('rate/<int:engagement_id>/', views.submit_rating, name='submit-rating'),
    path('endorse/<int:engagement_id>/', views.submit_endorsement, name='submit-endorsement'),
]
