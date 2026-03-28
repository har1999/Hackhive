from django.db import models
from django.conf import settings

class NotificationLog(models.Model):
    TYPE_CHOICES = [
        ('otp', 'OTP'), ('job_alert', 'Job Alert'), ('hired', 'Hired'),
        ('rating_reminder', 'Rating Reminder'), ('urgent_broadcast', 'Urgent Broadcast'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.TextField()
    sent_via = models.CharField(max_length=20, default='sms')
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications_log'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} → {self.user.phone}"
