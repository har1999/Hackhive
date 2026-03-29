from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Q

from jobs.models import Job, JobApplication, JobEngagement
from workers.models import WorkerProfile, FavouriteWorker
from ratings.models import Rating, SkillEndorsement
from accounts.models import User


@login_required
def dashboard(request):
    if not request.user.is_contractor:
        return redirect('worker_feed')

    active_jobs = Job.objects.filter(
        contractor=request.user, status='open'
    ).annotate(applicant_count=Count('applications')).order_by('-created_at')

    past_jobs = Job.objects.filter(
        contractor=request.user, status__in=['completed', 'cancelled']
    ).order_by('-created_at')[:5]

    favourites = FavouriteWorker.objects.filter(
        contractor=request.user
    ).select_related('worker__worker_profile')

    contractor_rating = Rating.objects.filter(
        contractor=request.user
    ).aggregate(avg=Avg('score'))['avg']

    recent_hires = JobEngagement.objects.filter(
        contractor=request.user
    ).select_related('worker', 'worker__worker_profile').order_by('-started_at')[:5]

    context = {
        'active_jobs': active_jobs,
        'past_jobs': past_jobs,
        'favourites': favourites,
        'contractor_rating': contractor_rating,
        'recent_hires': recent_hires,
    }
    return render(request, 'contractors/dashboard.html', context)


@login_required
def post_job(request):
    if not request.user.is_contractor:
        return redirect('worker_feed')

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

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        skill_category = request.POST.get('skill_category', '')
        location_name = request.POST.get('location_name', '').strip()
        duration_days = request.POST.get('duration_days', 1)
        daily_rate = request.POST.get('daily_rate', 0)
        workers_needed = request.POST.get('workers_needed', 1)
        is_urgent = request.POST.get('is_urgent') == 'on'
        description = request.POST.get('description', '').strip()
        start_date = request.POST.get('start_date', '')

        if not title or not skill_category or not location_name or not start_date:
            messages.error(request, 'Please fill in all required fields.')
        else:
            job = Job.objects.create(
                contractor=request.user,
                title=title,
                skill_category=skill_category,
                location_name=location_name,
                latitude=request.user.latitude or 19.0760,
                longitude=request.user.longitude or 72.8777,
                duration_days=int(duration_days),
                daily_rate=int(daily_rate),
                workers_needed=int(workers_needed),
                is_urgent=is_urgent,
                description=description,
                start_date=start_date,
                status='open',
            )
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('contractor_dashboard')

    return render(request, 'contractors/post_job.html', {'skill_choices': SKILL_CHOICES})


@login_required
def job_applicants(request, job_id):
    if not request.user.is_contractor:
        return redirect('worker_feed')

    job = get_object_or_404(Job, id=job_id, contractor=request.user)

    applicants = JobApplication.objects.filter(job=job).select_related(
        'worker', 'worker__worker_profile'
    ).annotate(
        avg_rating=Avg('worker__ratings_received__score'),
        completed_jobs=Count(
            'worker__engagements__id',
            filter=Q(worker__engagements__status='completed')
        )
    ).order_by('-avg_rating', '-applied_at')

    fav_ids = list(FavouriteWorker.objects.filter(
        contractor=request.user
    ).values_list('worker_id', flat=True))

    context = {
        'job': job,
        'applicants': applicants,
        'fav_ids': fav_ids,
    }
    return render(request, 'contractors/job_applicants.html', context)


@login_required
def hire_worker(request, application_id):
    if not request.user.is_contractor:
        return redirect('worker_feed')

    application = get_object_or_404(
        JobApplication, id=application_id, job__contractor=request.user
    )

    if request.method == 'POST':
        already_hired = JobEngagement.objects.filter(
            application=application
        ).exists()

        if not already_hired:
            JobEngagement.objects.create(
                application=application,
                job=application.job,
                worker=application.worker,
                contractor=request.user,
                status='in_progress',
            )
            application.status = 'hired'
            application.hired_at = timezone.now()
            application.save()

            # Reduce workers needed
            job = application.job
            if job.workers_needed > 0:
                job.workers_needed -= 1
                if job.workers_needed == 0:
                    job.status = 'active'
                job.save()

            messages.success(
                request,
                f'{application.worker.name} has been hired for "{application.job.title}"!'
            )
        else:
            messages.info(request, 'Worker is already hired for this job.')

    return redirect('job_applicants', job_id=application.job.id)


@login_required
def toggle_favourite(request, worker_id):
    if not request.user.is_contractor:
        return redirect('worker_feed')

    worker = get_object_or_404(User, id=worker_id, role='worker')
    fav, created = FavouriteWorker.objects.get_or_create(
        contractor=request.user, worker=worker
    )
    if not created:
        fav.delete()
        messages.success(request, f'{worker.name} removed from favourites.')
    else:
        messages.success(request, f'{worker.name} added to favourites!')

    next_url = request.POST.get('next') or request.GET.get('next') or 'contractor_dashboard'
    return redirect(next_url)


@login_required
def rate_worker(request, engagement_id):
    if not request.user.is_contractor:
        return redirect('worker_feed')

    engagement = get_object_or_404(
        JobEngagement, id=engagement_id, contractor=request.user, status='completed'
    )

    already_rated = Rating.objects.filter(
        engagement=engagement, contractor=request.user
    ).exists()

    if already_rated:
        messages.info(request, 'You have already rated this worker.')
        return redirect('contractor_dashboard')

    SKILL_TAGS = [
        'Reliable timekeeping', 'Can read technical drawings',
        'High finish quality', 'Works independently',
        'Good team player', 'Handles tools well', 'Follows safety protocols',
    ]

    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        review = request.POST.get('review', '').strip()
        endorsements = request.POST.getlist('endorsements')

        if not (1 <= score <= 5):
            messages.error(request, 'Please select a rating between 1 and 5.')
        else:
            Rating.objects.create(
                engagement=engagement,
                contractor=request.user,
                worker=engagement.worker,
                score=score,
                review=review,
            )
            for tag in endorsements:
                SkillEndorsement.objects.create(
                    engagement=engagement,
                    contractor=request.user,
                    worker=engagement.worker,
                    skill_tag=tag,
                )
            messages.success(request, 'Rating submitted successfully!')
            return redirect('contractor_dashboard')

    return render(request, 'contractors/rate_worker.html', {
        'engagement': engagement,
        'skill_tags': SKILL_TAGS,
    })


@login_required
def close_job(request, job_id):
    if not request.user.is_contractor:
        return redirect('worker_feed')

    job = get_object_or_404(Job, id=job_id, contractor=request.user)
    if request.method == 'POST':
        job.status = 'completed'
        job.save()
        JobEngagement.objects.filter(
            job=job, status='in_progress'
        ).update(status='completed', completed_at=timezone.now())
        messages.success(request, f'Job "{job.title}" has been closed.')

    return redirect('contractor_dashboard')