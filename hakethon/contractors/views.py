"""
Contractor Dashboard - KaamSetu
Post jobs, view applicants (sorted by trust), hire, manage.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.utils import timezone
from jobs.models import Job, JobApplication, JobEngagement, SKILL_CHOICES
from workers.models import WorkerProfile, FavouriteWorker
from .models import ContractorProfile


@login_required
def dashboard(request):
    if not request.user.is_contractor:
        return redirect('/worker/feed/')

    profile, _ = ContractorProfile.objects.get_or_create(user=request.user)

    active_jobs = Job.objects.filter(
        contractor=request.user, status__in=['open', 'active']
    ).annotate(app_count=Count('applications')).order_by('-created_at')

    completed_jobs = Job.objects.filter(
        contractor=request.user, status='completed'
    ).order_by('-updated_at')[:10]

    favourite_workers = FavouriteWorker.objects.filter(
        contractor=request.user
    ).select_related('worker', 'worker__worker_profile')

    recent_hires = JobEngagement.objects.filter(
        contractor=request.user
    ).select_related('worker', 'job').order_by('-started_at')[:10]

    return render(request, 'contractor/dashboard.html', {
        'profile': profile,
        'active_jobs': active_jobs,
        'completed_jobs': completed_jobs,
        'favourite_workers': favourite_workers,
        'recent_hires': recent_hires,
    })


@login_required
def post_job(request):
    if not request.user.is_contractor:
        return redirect('/worker/feed/')

    if request.method == 'POST':
        data = request.POST
        job = Job.objects.create(
            contractor=request.user,
            title=data.get('title'),
            skill_category=data.get('skill_category'),
            description=data.get('description', ''),
            location_name=data.get('location_name'),
            latitude=float(data.get('latitude', 19.076)),
            longitude=float(data.get('longitude', 72.877)),
            daily_rate=int(data.get('daily_rate', 500)),
            workers_needed=int(data.get('workers_needed', 1)),
            duration_days=int(data.get('duration_days', 1)),
            start_date=data.get('start_date'),
            is_urgent=data.get('is_urgent') == 'on',
            radius_km=int(data.get('radius_km', 10)),
        )
        if job.is_urgent:
            # Trigger async broadcast
            try:
                from notifications.tasks import broadcast_urgent_job
                broadcast_urgent_job.delay(job.id)
            except Exception:
                pass  # Celery not running in dev — OK
            messages.success(request, f'Urgent job posted! Broadcast sent to nearby workers.')
        else:
            messages.success(request, f'Job "{job.title}" posted successfully!')
        return redirect(f'/contractor/job/{job.id}/applicants/')

    return render(request, 'contractor/post_job.html', {'skill_choices': SKILL_CHOICES})


@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, contractor=request.user)

    # Smart sort: past collaborator > relevant job count > avg rating
    applications = JobApplication.objects.filter(
        job=job
    ).select_related('worker', 'worker__worker_profile').annotate(
        avg_rating=Avg('worker__ratings_received__score'),
        completed_jobs=Count(
            'worker__engagements',
            filter=Q(worker__engagements__status='completed')
        )
    ).order_by('-status', '-avg_rating', '-completed_jobs')

    # Flag past collaborators
    past_worker_ids = JobEngagement.objects.filter(
        contractor=request.user
    ).values_list('worker_id', flat=True)

    favourite_ids = FavouriteWorker.objects.filter(
        contractor=request.user
    ).values_list('worker_id', flat=True)

    for app in applications:
        app.is_past_collaborator = app.worker_id in past_worker_ids
        app.is_favourite = app.worker_id in favourite_ids

    return render(request, 'contractor/applicants.html', {
        'job': job,
        'applications': applications,
    })


@login_required
def hire_worker(request, application_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    application = get_object_or_404(
        JobApplication, id=application_id, job__contractor=request.user
    )

    if application.status != 'pending':
        return JsonResponse({'error': 'Application already processed'}, status=400)

    application.status = 'hired'
    application.hired_at = timezone.now()
    application.save()

    engagement = JobEngagement.objects.create(
        application=application,
        job=application.job,
        worker=application.worker,
        contractor=request.user,
    )

    # SMS the worker
    try:
        from notifications.sms import send_hired_sms
        send_hired_sms(
            application.worker.phone,
            application.job.title,
            request.user.name,
            application.job.start_date
        )
    except Exception:
        pass

    return JsonResponse({'success': True, 'engagement_id': engagement.id})


@login_required
def toggle_favourite(request, worker_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    worker = get_object_or_404(User, id=worker_id, role='worker')
    fav, created = FavouriteWorker.objects.get_or_create(
        contractor=request.user, worker=worker
    )
    if not created:
        fav.delete()
        return JsonResponse({'favourited': False})
    return JsonResponse({'favourited': True})
