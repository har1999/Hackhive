"""
Ratings & Endorsements Models
Tied directly to the JobEngagement to prove the work was actually done.
"""
from django.db import models
from django.conf import settings
from jobs.models import JobEngagement

# This is the missing list that caused the ImportError
ENDORSEMENT_TAGS = [
    'Excellent Finish',
    'Always on time',
    'Reads Technical Drawings',
    'Good Communication',
    'Follows Safety Rules',
    'Fast Worker',
    'Problem Solver'
]

class Rating(models.Model):
    engagement = models.OneToOneField(JobEngagement, on_delete=models.CASCADE, related_name='rating')
    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_given')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_received')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="1 to 5 stars")
    review = models.TextField(blank=True, help_text="Optional written feedback")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ratings_rating'

    def __str__(self):
        return f"{self.score} Stars for {self.worker.name} by {self.contractor.name}"


class SkillEndorsement(models.Model):
    """Specific skills demonstrated during a specific job."""
    engagement = models.ForeignKey(JobEngagement, on_delete=models.CASCADE, related_name='endorsements')
    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='endorsements_received')
    skill_tag = models.CharField(max_length=100) # e.g., "Excellent Tiling Finish", "Always on time"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ratings_skill_endorsement'

    def __str__(self):
        return f"'{self.skill_tag}' for {self.worker.name}"