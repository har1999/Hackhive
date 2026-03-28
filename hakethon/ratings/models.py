"""
Ratings & Endorsements - KaamSetu
Immutable after submission. Trust built from the bottom up.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


ENDORSEMENT_TAGS = [
    ('reads_plans', 'Can read technical drawings'),
    ('tiling_quality', 'Tiling finish quality is high'),
    ('punctual', 'Reliable timekeeping'),
    ('plastering', 'Plastering finish is smooth'),
    ('clean_work', 'Keeps worksite clean'),
    ('team_player', 'Works well in a team'),
    ('electrical_safe', 'Follows electrical safety'),
    ('plumbing_neat', 'Plumbing work is neat'),
    ('fast_worker', 'Works quickly without errors'),
    ('tools_care', 'Takes care of tools and materials'),
]


class Rating(models.Model):
    """
    Mutual rating after job completion.
    IMMUTABLE: no update/delete after creation. This is by design.
    """
    RATER_WORKER = 'worker'
    RATER_CONTRACTOR = 'contractor'
    DIRECTION_CHOICES = [
        ('worker_to_contractor', 'Worker rates Contractor'),
        ('contractor_to_worker', 'Contractor rates Worker'),
    ]

    engagement = models.ForeignKey(
        'jobs.JobEngagement', on_delete=models.CASCADE, related_name='ratings'
    )
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_given'
    )
    ratee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_received'
    )
    direction = models.CharField(max_length=30, choices=DIRECTION_CHOICES)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    note = models.CharField(max_length=280, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ratings_rating'
        unique_together = [('engagement', 'direction')]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rater.name} → {self.ratee.name}: {self.score}★"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Ratings cannot be edited after submission.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Ratings cannot be deleted.")


class SkillEndorsement(models.Model):
    """
    Contractor endorses specific skills observed during the job.
    Tagged to the specific engagement — not floating praise.
    """
    engagement = models.ForeignKey(
        'jobs.JobEngagement', on_delete=models.CASCADE, related_name='endorsements'
    )
    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='endorsements_given',
        limit_choices_to={'role': 'contractor'}
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='endorsements_received',
        limit_choices_to={'role': 'worker'}
    )
    tag = models.CharField(max_length=50, choices=ENDORSEMENT_TAGS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ratings_endorsement'
        unique_together = [('engagement', 'tag')]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contractor.name} endorses {self.worker.name}: {self.tag}"

    @property
    def tag_label(self):
        return dict(ENDORSEMENT_TAGS).get(self.tag, self.tag)
