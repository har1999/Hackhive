"""
Jobs Views - KaamSetu
Job feed (worker), post job (contractor), apply, hire, complete.
"""
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from .models import Job, JobApplication, JobEngagement, PhotoEvidence, SKILL_CHOICES
from workers.models import WorkerProfile


def haversine_filter(jobs, lat, lng, radius_km):
    """Filter jobs within radius using Haversine. Used when no PostGIS."""
    result = []
    for job in jobs:
        dist = job.distance_from(lat, lng)
        if dist <= radius_km:
            job.distance_km = round(dist, 1)
            result.append(job)
    result.sort(key=lambda j: j._distance_km)
    return result


@login_required
def worker_job_feed(request):
    """
    Worker's job feed — filtered by skill + location radius.
    Cards are icon-heavy, minimal text.
    """
    if not request.user.is_worker:
        return redirect('/contractor/dashboard/')

    profile, _ = WorkerProfile.objects.get_or_create(user=request.user)

    lat = request.GET.get('lat') or profile.latitude
    lng = request.GET.get('lng') or profile.longitude
    skill = request.GET.get('skill') or profile.skill_category
    radius = int(request.GET.get('radius') or profile.preferred_radius_km or 15)

    jobs_qs = Job.objects.filter(
        status='open',
        skill_category=skill
    ).select_related('contractor').order_by('-is_urgent', '-created_at')

    nearby_jobs = []
    applied_ids = set(
        JobApplication.objects.filter(worker=request.user).values_list('job_id', flat=True)
    )

    if lat and lng:
        nearby_jobs = haversine_filter(list(jobs_qs), float(lat), float(lng), radius)
    else:
        nearby_jobs = list(jobs_qs[:50])
        for j in nearby_jobs:
            j._distance_km = None

    return render(request, 'worker/feed.html', {
        'jobs': nearby_jobs,
        'skill_choices': SKILL_CHOICES,
        'selected_skill': skill,
        'applied_ids': applied_ids,
        'profile': profile,
        'radius': radius,
    })


@login_required
def apply_to_job(request, job_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    job = get_object_or_404(Job, id=job_id, status='open')
    app, created = JobApplication.objects.get_or_create(
        job=job, worker=request.user,
        defaults={'status': 'pending'}
    )
    if not created:
        return JsonResponse({'error': 'Already applied'}, status=400)

    # Notify contractor (async in prod)
    messages.success(request, f'Applied to {job.title}!')
    return JsonResponse({'success': True, 'message': 'Applied successfully!'})


@login_required
def worker_my_jobs(request):
    if not request.user.is_worker:
        return redirect('/contractor/dashboard/')

    applications = JobApplication.objects.filter(
        worker=request.user
    ).select_related('job', 'job__contractor').order_by('-applied_at')

    engagements = JobEngagement.objects.filter(
        worker=request.user
    ).select_related('job', 'contractor').order_by('-started_at')

    return render(request, 'worker/my_jobs.html', {
        'applications': applications,
        'engagements': engagements,
    })


@login_required
def worker_profile_view(request, user_id=None):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if user_id:
        target_user = get_object_or_404(User, id=user_id, role='worker')
    else:
        target_user = request.user

    profile, _ = WorkerProfile.objects.get_or_create(user=target_user)

    completed_engagements = JobEngagement.objects.filter(
        worker=target_user, status='completed'
    ).select_related('job', 'contractor').prefetch_related(
        'ratings', 'endorsements', 'photos'
    ).order_by('-completed_at')

    # Rating breakdown
    ratings_received = target_user.ratings_received.filter(
        direction='contractor_to_worker'
    ).order_by('-created_at')

    endorsements = target_user.endorsements_received.select_related(
        'contractor', 'engagement__job'
    ).order_by('-created_at')

    return render(request, 'worker/profile.html', {
        'profile': profile,
        'target_user': target_user,
        'completed_engagements': completed_engagements,
        'ratings': ratings_received,
        'endorsements': endorsements,
        'is_own_profile': target_user == request.user,
    })


@login_required
def mark_job_complete(request, engagement_id):
    engagement = get_object_or_404(JobEngagement, id=engagement_id)

    if request.user == engagement.worker:
        engagement.worker_marked_complete = True
    elif request.user == engagement.contractor:
        engagement.contractor_marked_complete = True
    else:
        messages.error(request, 'Not authorized')
        return redirect('back')

    engagement.save()
    completed = engagement.check_and_complete()
    if completed:
        messages.success(request, 'Job completed! Please rate your experience.')
    else:
        messages.info(request, 'Marked complete. Waiting for the other party to confirm.')

    if request.user.is_worker:
        return redirect('/worker/my-jobs/')
    return redirect('/contractor/dashboard/')
