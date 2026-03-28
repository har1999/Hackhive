"""
Worker Profile - KaamSetu
Built through work, not claims.
The profile IS the job history.
"""
from django.db import models
from django.conf import settings
from jobs.models import SKILL_CHOICES


class WorkerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='worker_profile'
    )
    skill_category = models.CharField(max_length=30, choices=SKILL_CHOICES, blank=True)
    secondary_skills = models.JSONField(default=list, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True, db_index=True)
    preferred_radius_km = models.PositiveIntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workers_profile'

    def __str__(self):
        return f"Worker: {self.user.name} ({self.skill_category})"

    @property
    def total_jobs(self):
        return self.user.engagements.filter(status='completed').count()

    @property
    def unique_contractors(self):
        return self.user.engagements.filter(status='completed').values('contractor').distinct().count()

    @property
    def average_rating(self):
        from django.db.models import Avg
        result = self.user.ratings_received.filter(
            direction='contractor_to_worker'
        ).aggregate(avg=Avg('score'))
        return round(result['avg'] or 0, 1)

    @property
    def trust_level(self):
        jobs = self.total_jobs
        if jobs == 0: return 'new'
        if jobs < 5: return 'emerging'
        if jobs < 15: return 'established'
        return 'verified'

    @property
    def trust_score(self):
        """
        Weighted trust score (0-100).
        Components:
        - Average rating (0-5) → weighted 50%
        - Unique contractors → up to 20 pts
        - Endorsement count → up to 20 pts
        - Recency boost → up to 10 pts
        """
        from django.db.models import Avg, Count
        from django.utils import timezone

        jobs = self.total_jobs
        if jobs == 0:
            return 0

        avg_rating = self.average_rating
        rating_score = (avg_rating / 5) * 50

        contractors = min(self.unique_contractors, 10)
        contractor_score = contractors * 2

        endorsement_count = min(self.user.endorsements_received.count(), 20)
        endorsement_score = endorsement_count * 1

        # Recency: any job in last 30 days
        from jobs.models import JobEngagement
        recent = JobEngagement.objects.filter(
            worker=self.user,
            status='completed',
            completed_at__gte=timezone.now() - timezone.timedelta(days=30)
        ).exists()
        recency_score = 10 if recent else 0

        return round(rating_score + contractor_score + endorsement_score + recency_score)


class FavouriteWorker(models.Model):
    """Contractor bookmarks a worker for easy repeat hiring."""
    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites',
        limit_choices_to={'role': 'contractor'}
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourited_by',
        limit_choices_to={'role': 'worker'}
    )
    added_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'workers_favourite'
        unique_together = [('contractor', 'worker')]

    def __str__(self):
        return f"{self.contractor.name} ♥ {self.worker.name}"
