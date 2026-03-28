"""
Celery async tasks for KaamSetu.
Handles SMS broadcasts, reminders, notifications.
"""
import logging
import math
logger = logging.getLogger(__name__)

# Try import celery — graceful fallback if not running
try:
    from celery import shared_task
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    def shared_task(f): return f


@shared_task
def broadcast_urgent_job(job_id):
    """
    Broadcast urgent job to all eligible workers within radius.
    Priority: past collaborators first → then all nearby workers.
    """
    from jobs.models import Job
    from workers.models import WorkerProfile
    from notifications.sms import send_urgent_broadcast_sms
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return

    workers = WorkerProfile.objects.filter(
        skill_category=job.skill_category,
        is_available=True,
        latitude__isnull=False,
        longitude__isnull=False,
    ).select_related('user')

    # Past collaborators
    past_worker_ids = job.contractor.contractor_engagements.values_list('worker_id', flat=True)

    eligible = []
    for wp in workers:
        dist = _haversine(job.latitude, job.longitude, wp.latitude, wp.longitude)
        if dist <= job.radius_km:
            eligible.append((wp, dist, wp.user_id in past_worker_ids))

    # Sort: past collaborators first
    eligible.sort(key=lambda x: (not x[2], x[1]))

    for wp, dist, is_past in eligible[:200]:  # Cap at 200 per broadcast
        send_urgent_broadcast_sms(
            wp.user.phone, job.title, job.location_name, job.daily_rate
        )
        logger.info(f"Urgent broadcast sent to {wp.user.phone}")

    job.broadcast_sent = True
    job.save()


@shared_task
def send_rating_reminder(engagement_id):
    """24hr reminder after job completion to submit ratings."""
    from jobs.models import JobEngagement
    from ratings.models import Rating
    from notifications.sms import _send

    try:
        eng = JobEngagement.objects.get(id=engagement_id, status='completed')
    except JobEngagement.DoesNotExist:
        return

    if not Rating.objects.filter(engagement=eng, direction='contractor_to_worker').exists():
        _send(eng.contractor.phone, f"KaamSetu: Please rate {eng.worker.name} for the job {eng.job.title}", 'rating_reminder')

    if not Rating.objects.filter(engagement=eng, direction='worker_to_contractor').exists():
        _send(eng.worker.phone, f"KaamSetu: Please rate contractor {eng.contractor.name} for {eng.job.title}", 'rating_reminder')


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    la1, lo1 = math.radians(lat1), math.radians(lon1)
    la2, lo2 = math.radians(lat2), math.radians(lon2)
    return R * 2 * math.asin(math.sqrt(
        math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    ))
