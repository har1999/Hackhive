from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ContractorProfileForm,
    EngagementRatingForm,
    FavoriteWorkerForm,
    JobApplyForm,
    JobPostingForm,
    WorkerProfileForm,
)
from .models import ContractorProfile, FavoriteWorker, JobApplication, JobEngagement, JobPosting, WorkerProfile


def _get_selected_worker(request):
    worker_id = request.GET.get('worker')
    queryset = WorkerProfile.objects.all().order_by('-created_at')
    if worker_id:
        return queryset.filter(id=worker_id).first()
    return queryset.first()


def _get_selected_contractor(request):
    contractor_id = request.GET.get('contractor')
    queryset = ContractorProfile.objects.all().order_by('-created_at')
    if contractor_id:
        return queryset.filter(id=contractor_id).first()
    return queryset.first()


def home(request):
    jobs = JobPosting.objects.filter(status=JobPosting.Status.OPEN).order_by('-urgent_same_day', '-created_at')[:6]
    context = {
        'jobs': jobs,
        'impact_stats': [
            {'label': 'Workers onboarded', 'value': WorkerProfile.objects.count()},
            {'label': 'Verified job entries', 'value': JobEngagement.objects.count()},
            {'label': 'Open opportunities', 'value': JobPosting.objects.filter(status=JobPosting.Status.OPEN).count()},
            {'label': 'Repeat contractor hires', 'value': FavoriteWorker.objects.count()},
        ],
    }
    return render(request, 'core/home.html', context)


def worker_profile(request):
    if request.method == 'POST' and request.POST.get('action') == 'register_worker':
        form = WorkerProfileForm(request.POST, prefix='worker')
        if form.is_valid():
            worker = form.save()
            messages.success(request, 'Worker profile created successfully.')
            return redirect(f"/worker/?worker={worker.id}")
        worker_form = form
    else:
        worker_form = WorkerProfileForm(prefix='worker')

    worker = _get_selected_worker(request)
    workers = WorkerProfile.objects.all().order_by('name')
    history = []
    worker_snapshot = None

    if worker:
        records = (
            JobEngagement.objects.filter(worker=worker)
            .select_related('job', 'contractor')
            .prefetch_related('endorsements')
            .order_by('-completed_on')
        )
        for item in records:
            history.append(
                {
                    'job': item.job.title,
                    'date': item.completed_on,
                    'contractor': item.contractor.name,
                    'rating': item.contractor_rating_for_worker,
                    'note': item.note_for_worker,
                    'endorsements': [endorsement.skill_tag for endorsement in item.endorsements.all()],
                }
            )
        worker_stats = records.aggregate(avg=Avg('contractor_rating_for_worker'), total=Count('id'))
        worker_snapshot = {
            'name': worker.name,
            'phone': worker.phone_number,
            'location': worker.location,
            'primary_skill': worker.primary_skill,
            'avg_rating': round(worker_stats['avg'] or 0.0, 2),
            'jobs_completed': worker_stats['total'],
        }

    context = {
        'worker': worker_snapshot,
        'history': history,
        'worker_form': worker_form,
        'workers': workers,
        'selected_worker_id': worker.id if worker else None,
    }
    return render(request, 'core/worker_profile.html', context)


def job_board(request):
    selected_skill = request.GET.get('skill', '')
    urgent_only = request.GET.get('urgent') == '1'

    jobs = JobPosting.objects.filter(status=JobPosting.Status.OPEN).select_related('contractor').order_by(
        '-urgent_same_day',
        '-created_at',
    )
    if selected_skill:
        jobs = jobs.filter(skill_required=selected_skill)
    if urgent_only:
        jobs = jobs.filter(urgent_same_day=True)

    if request.method == 'POST' and request.POST.get('action') == 'apply':
        job = get_object_or_404(JobPosting, id=request.POST.get('job_id'), status=JobPosting.Status.OPEN)
        apply_form = JobApplyForm(request.POST, skill=job.skill_required, prefix=f'job-{job.id}')
        if apply_form.is_valid():
            worker = apply_form.cleaned_data['worker']
            application, created = JobApplication.objects.get_or_create(
                job=job,
                worker=worker,
                defaults={'status': JobApplication.Status.APPLIED},
            )
            if created:
                messages.success(request, 'Application submitted.')
            else:
                messages.info(request, 'Application already exists for this worker and job.')
            query_string = request.META.get('QUERY_STRING', '')
            if query_string:
                return redirect(f"{request.path}?{query_string}")
            return redirect(request.path)
        messages.error(request, 'Could not submit application. Check selected worker.')

    for job in jobs:
        job.apply_form = JobApplyForm(skill=job.skill_required, prefix=f'job-{job.id}')

    context = {
        'selected_skill': selected_skill or 'All Skills',
        'radius_km': 10,
        'jobs': jobs,
        'urgent_only': urgent_only,
    }
    return render(request, 'core/job_board.html', context)


def contractor_dashboard(request):
    contractor = _get_selected_contractor(request)

    contractor_form = ContractorProfileForm(prefix='contractor')
    job_form = JobPostingForm(prefix='job')
    rating_form = EngagementRatingForm(prefix='rate', contractor=contractor)
    favorite_form = FavoriteWorkerForm(prefix='fav')

    if contractor:
        favorite_form.fields['worker'].queryset = WorkerProfile.objects.filter(
            applications__job__contractor=contractor,
            applications__status=JobApplication.Status.ACCEPTED,
        ).distinct()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'register_contractor':
            contractor_form = ContractorProfileForm(request.POST, prefix='contractor')
            if contractor_form.is_valid():
                new_contractor = contractor_form.save()
                messages.success(request, 'Contractor profile created.')
                return redirect(f"/contractor/dashboard/?contractor={new_contractor.id}")

        if action == 'create_job' and contractor:
            job_form = JobPostingForm(request.POST, prefix='job')
            if job_form.is_valid():
                job = job_form.save(commit=False)
                job.contractor = contractor
                job.save()
                messages.success(request, 'Job posted successfully.')
                return redirect(request.get_full_path())

        if action == 'set_application_status' and contractor:
            application = get_object_or_404(
                JobApplication,
                id=request.POST.get('application_id'),
                job__contractor=contractor,
            )
            new_status = request.POST.get('status', JobApplication.Status.APPLIED)
            if new_status in JobApplication.Status.values:
                application.status = new_status
                application.save(update_fields=['status'])
                messages.success(request, 'Application status updated.')
            return redirect(request.get_full_path())

        if action == 'close_job' and contractor:
            job = get_object_or_404(JobPosting, id=request.POST.get('job_id'), contractor=contractor)
            job.status = JobPosting.Status.CLOSED
            job.save(update_fields=['status'])
            messages.success(request, 'Job closed.')
            return redirect(request.get_full_path())

        if action == 'add_rating' and contractor:
            rating_form = EngagementRatingForm(request.POST, prefix='rate', contractor=contractor)
            job_id = request.POST.get('job_id')
            job = JobPosting.objects.filter(id=job_id, contractor=contractor, status=JobPosting.Status.CLOSED).first()
            if rating_form.is_valid() and job:
                engagement = rating_form.save(commit=False)
                engagement.job = job
                engagement.contractor = contractor
                try:
                    engagement.save()
                    rating_form.save_endorsements(engagement)
                    messages.success(request, 'Mutual rating recorded with endorsements.')
                    return redirect(request.get_full_path())
                except Exception as exc:
                    messages.error(request, str(exc))
            else:
                messages.error(request, 'Choose a closed job and valid worker to submit rating.')

        if action == 'add_favorite' and contractor:
            favorite_form = FavoriteWorkerForm(request.POST, prefix='fav')
            favorite_form.fields['worker'].queryset = WorkerProfile.objects.filter(
                applications__job__contractor=contractor,
                applications__status=JobApplication.Status.ACCEPTED,
            ).distinct()
            if favorite_form.is_valid():
                worker = favorite_form.cleaned_data['worker']
                FavoriteWorker.objects.get_or_create(contractor=contractor, worker=worker)
                messages.success(request, 'Worker added to favorites.')
                return redirect(request.get_full_path())

    contractors = ContractorProfile.objects.all().order_by('name')

    active_postings = []
    applicants = []
    past_hires = []
    closed_jobs = []
    if contractor:
        active_postings = contractor.jobs.filter(status=JobPosting.Status.OPEN).order_by('-created_at')
        closed_jobs = contractor.jobs.filter(status=JobPosting.Status.CLOSED).order_by('-created_at')

        worker_metrics = {
            row['worker_id']: row
            for row in JobEngagement.objects.filter(worker__applications__job__contractor=contractor)
            .values('worker_id')
            .annotate(jobs_done=Count('id'), avg_rating=Avg('contractor_rating_for_worker'))
        }

        app_qs = (
            JobApplication.objects.filter(job__contractor=contractor)
            .select_related('worker', 'job')
            .order_by('status', '-created_at')
        )
        for app in app_qs:
            metrics = worker_metrics.get(app.worker_id, {'jobs_done': 0, 'avg_rating': 0})
            applicants.append(
                {
                    'application_id': app.id,
                    'name': app.worker.name,
                    'skill': app.worker.primary_skill,
                    'jobs_done': metrics['jobs_done'],
                    'avg_rating': round(metrics['avg_rating'] or 0.0, 2),
                    'status': app.status,
                    'job_title': app.job.title,
                }
            )

        past_qs = (
            JobEngagement.objects.filter(contractor=contractor)
            .select_related('worker', 'job')
            .order_by('-completed_on')
        )
        for entry in past_qs:
            past_hires.append(
                {
                    'worker': entry.worker.name,
                    'skill': entry.worker.primary_skill,
                    'job': entry.job.title,
                    'rating': entry.contractor_rating_for_worker,
                }
            )

    context = {
        'contractor': contractor,
        'contractor_rating': contractor.avg_rating if contractor else 0,
        'active_postings': active_postings,
        'applicants': applicants,
        'past_hires': past_hires,
        'contractor_form': contractor_form,
        'job_form': job_form,
        'rating_form': rating_form,
        'favorite_form': favorite_form,
        'contractors': contractors,
        'selected_contractor_id': contractor.id if contractor else None,
        'closed_jobs': closed_jobs,
    }
    return render(request, 'core/contractor_dashboard.html', context)


def voice_ui(request):
    workers = WorkerProfile.objects.count()
    open_jobs = JobPosting.objects.filter(status=JobPosting.Status.OPEN).count()
    context = {
        'workers': workers,
        'open_jobs': open_jobs,
    }
    return render(request, 'core/voice_ui.html', context)
