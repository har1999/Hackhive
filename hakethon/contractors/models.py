"""
Contractor Profile - KaamSetu
Contractors are also accountable. Their rating is public.
"""
from django.db import models
from django.conf import settings


class ContractorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contractor_profile'
    )
    company_name = models.CharField(max_length=200, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    gst_number = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contractors_profile'

    def __str__(self):
        return f"Contractor: {self.user.name}"

    @property
    def total_jobs_posted(self):
        return self.user.posted_jobs.count()

    @property
    def total_workers_hired(self):
        from jobs.models import JobEngagement
        return JobEngagement.objects.filter(contractor=self.user).count()

    @property
    def average_rating(self):
        from django.db.models import Avg
        result = self.user.ratings_received.filter(
            direction='worker_to_contractor'
        ).aggregate(avg=Avg('score'))
        return round(result['avg'] or 0, 1)

    @property
    def pays_on_time_score(self):
        """Average from worker ratings — transparency."""
        return self.average_rating
