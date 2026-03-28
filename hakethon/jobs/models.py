"""
Jobs Models - KaamSetu
Core of the platform. Jobs connect workers to contractors.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
import math


SKILL_CHOICES = [
    ('mason', 'Mason / Mistri'),
    ('electrician', 'Electrician'),
    ('plumber', 'Plumber'),
    ('painter', 'Painter'),
    ('carpenter', 'Carpenter'),
    ('labourer', 'General Labourer'),
    ('welder', 'Welder'),
    ('tiler', 'Tiler'),
    ('fabricator', 'Fabricator'),
    ('rebar', 'Rebar Worker'),
]

SKILL_ICONS = {
    'mason': '🧱', 'electrician': '⚡', 'plumber': '🔧', 'painter': '🎨',
    'carpenter': '🪚', 'labourer': '👷', 'welder': '🔥', 'tiler': '⬜',
    'fabricator': '⚙️', 'rebar': '🏗️',
}


class Job(models.Model):
    STATUS_OPEN = 'open'
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='posted_jobs', limit_choices_to={'role': 'contractor'}
    )
    title = models.CharField(max_length=200)
    skill_category = models.CharField(max_length=30, choices=SKILL_CHOICES, db_index=True)
    description = models.TextField(blank=True)
    location_name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius_km = models.PositiveIntegerField(default=10, help_text='Visible to workers within this radius')
    daily_rate = models.PositiveIntegerField(help_text='Rate in INR per day')
    workers_needed = models.PositiveIntegerField(default=1)
    duration_days = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    is_urgent = models.BooleanField(default=False, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    broadcast_sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'jobs_job'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['skill_category', 'status']),
            models.Index(fields=['is_urgent', 'status']),
        ]

    def __str__(self):
        return f"{self.title} ({self.skill_category}) — {self.location_name}"

    def distance_from(self, lat, lng):
        """Haversine distance in km."""
        R = 6371
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(lat), math.radians(lng)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    @property
    def skill_icon(self):
        return SKILL_ICONS.get(self.skill_category, '🔨')

    @property
    def total_earning(self):
        return self.daily_rate * self.duration_days

    @property
    def applications_count(self):
        return self.applications.count()


class JobApplication(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_HIRED = 'hired'
    STATUS_REJECTED = 'rejected'
    STATUS_WITHDRAWN = 'withdrawn'
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='applications', limit_choices_to={'role': 'worker'}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    hired_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'jobs_application'
        unique_together = [('job', 'worker')]
        ordering = ['-applied_at']

    def hire(self):
        if self.status != self.STATUS_HIRED and self.job.workers_needed > 0:
            self.status = self.STATUS_HIRED
            self.hired_at = timezone.now()
            self.job.workers_needed -= 1
            self.job.save()
            self.save()

    def __str__(self):
        return f"{self.worker.name} → {self.job.title} [{self.status}]"


class JobEngagement(models.Model):
    """Confirmed hire. Tracks the actual work done. Source of truth for ratings."""
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_DISPUTED = 'disputed'
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('disputed', 'Disputed'),
    ]

    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='engagement')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='engagements')
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='engagements'
    )
    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contractor_engagements'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    contractor_marked_complete = models.BooleanField(default=False)
    worker_marked_complete = models.BooleanField(default=False)

    class Meta:
        db_table = 'jobs_engagement'
        ordering = ['-started_at']

    def __str__(self):
        return f"Engagement: {self.worker.name} @ {self.job.title}"

    def check_and_complete(self):
        if self.contractor_marked_complete and self.worker_marked_complete:
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()
            return True
        return False


class PhotoEvidence(models.Model):
    """Photos attached to a completed engagement. Visual proof of work."""
    engagement = models.ForeignKey(JobEngagement, on_delete=models.CASCADE, related_name='photos')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='evidence/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jobs_photo'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Photo: {self.engagement}"
