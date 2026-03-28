from django.core.exceptions import ValidationError
from django.db import models


class SkillCategory(models.TextChoices):
    MASON = 'Mason', 'Mason'
    ELECTRICIAN = 'Electrician', 'Electrician'
    PAINTER = 'Painter', 'Painter'
    LABOURER = 'Labourer', 'Labourer'
    TILER = 'Tiler', 'Tiler'


class WorkerProfile(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20, unique=True)
    primary_skill = models.CharField(max_length=20, choices=SkillCategory.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.primary_skill})"


class ContractorProfile(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def avg_rating(self):
        data = self.received_ratings.aggregate(avg=models.Avg('worker_rating_for_contractor'))
        return round(data['avg'] or 0.0, 2)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'

    contractor = models.ForeignKey(
        ContractorProfile,
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    title = models.CharField(max_length=200)
    skill_required = models.CharField(max_length=20, choices=SkillCategory.choices)
    location = models.CharField(max_length=120)
    duration_days = models.PositiveIntegerField(default=1)
    daily_rate = models.PositiveIntegerField()
    workers_needed = models.PositiveIntegerField(default=1)
    radius_km = models.PositiveIntegerField(default=10)
    urgent_same_day = models.BooleanField(default=False)
    start_date = models.DateField()
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"


class JobApplication(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.APPLIED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job', 'worker'], name='unique_worker_application_per_job'),
        ]

    def __str__(self):
        return f"{self.worker.name} -> {self.job.title}"


class JobEngagement(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='engagements')
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name='engagements')
    contractor = models.ForeignKey(
        ContractorProfile,
        on_delete=models.CASCADE,
        related_name='received_ratings',
    )
    completed_on = models.DateField()
    contractor_rating_for_worker = models.PositiveSmallIntegerField()
    worker_rating_for_contractor = models.PositiveSmallIntegerField()
    note_for_worker = models.CharField(max_length=180, blank=True)
    note_for_contractor = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(contractor_rating_for_worker__gte=1)
                & models.Q(contractor_rating_for_worker__lte=5),
                name='contractor_rating_worker_range',
            ),
            models.CheckConstraint(
                check=models.Q(worker_rating_for_contractor__gte=1)
                & models.Q(worker_rating_for_contractor__lte=5),
                name='worker_rating_contractor_range',
            ),
            models.UniqueConstraint(fields=['job', 'worker'], name='unique_engagement_per_job_worker'),
        ]

    def clean(self):
        if self.pk:
            original = JobEngagement.objects.get(pk=self.pk)
            blocked_fields = [
                'contractor_rating_for_worker',
                'worker_rating_for_contractor',
                'note_for_worker',
                'note_for_contractor',
            ]
            for field_name in blocked_fields:
                if getattr(original, field_name) != getattr(self, field_name):
                    raise ValidationError('Ratings cannot be edited once submitted.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job.title} - {self.worker.name}"


class SkillEndorsement(models.Model):
    engagement = models.ForeignKey(JobEngagement, on_delete=models.CASCADE, related_name='endorsements')
    skill_tag = models.CharField(max_length=80)
    note = models.CharField(max_length=180, blank=True)

    def __str__(self):
        return self.skill_tag


class FavoriteWorker(models.Model):
    contractor = models.ForeignKey(ContractorProfile, on_delete=models.CASCADE, related_name='favorites')
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name='favored_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['contractor', 'worker'], name='unique_contractor_favorite_worker'),
        ]

    def __str__(self):
        return f"{self.contractor.name} likes {self.worker.name}"
