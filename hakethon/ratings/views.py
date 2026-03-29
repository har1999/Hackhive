"""
Ratings Views - KaamSetu
Submit ratings and endorsements after job completion.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rating, SkillEndorsement, ENDORSEMENT_TAGS
from jobs.models import JobEngagement


@login_required
def submit_rating(request, engagement_id):
    engagement = get_object_or_404(JobEngagement, id=engagement_id, status='completed')

    # Verify user is part of this engagement
    if request.user not in [engagement.worker, engagement.contractor]:
        messages.error(request, 'Not authorized.')
        return redirect('/')

    # Workers rate contractors, contractors rate workers
    # Rating.contractor = who gave the rating (always the contractor field)
    # We use a separate WorkerRating concept via the same model:
    # contractor_to_worker: contractor=eng.contractor, worker=eng.worker
    # worker_to_contractor: we store contractor=eng.contractor, worker=eng.worker
    #   but check a separate already_rated flag per user

    if request.user == engagement.contractor:
        # Contractor rating the worker
        already_rated = Rating.objects.filter(
            engagement=engagement,
            contractor=engagement.contractor
        ).exists()
        if already_rated:
            messages.info(request, 'You have already rated this worker.')
            return redirect('contractor_dashboard')

        if request.method == 'POST':
            score = int(request.POST.get('score', 0))
            review = request.POST.get('review', '').strip()[:280]
            if not 1 <= score <= 5:
                messages.error(request, 'Score must be between 1 and 5.')
            else:
                Rating.objects.create(
                    engagement=engagement,
                    contractor=engagement.contractor,
                    worker=engagement.worker,
                    score=score,
                    review=review,
                )
                messages.success(request, 'Rating submitted!')
                return redirect('contractor_dashboard')

        return render(request, 'shared/rate.html', {
            'engagement': engagement,
            'ratee': engagement.worker,
            'is_contractor': True,
            'endorsement_tags': ENDORSEMENT_TAGS,
        })

    else:
        # Worker rating the contractor — we don't have a separate model for this
        # Store in same Rating table but check by worker to avoid double submit
        # Since unique_together is (engagement, contractor) we use a simple session flag
        # Better: use a separate flag on engagement or check ratings by worker
        already_rated = Rating.objects.filter(
            engagement=engagement,
            worker=engagement.worker,
            contractor=engagement.contractor,
            review__startswith='[worker-review]'
        ).exists()

        if already_rated:
            messages.info(request, 'You have already rated this contractor.')
            return redirect('/worker/my-jobs/')

        if request.method == 'POST':
            score = int(request.POST.get('score', 0))
            review = request.POST.get('review', '').strip()[:280]
            if not 1 <= score <= 5:
                messages.error(request, 'Score must be between 1 and 5.')
            else:
                # Tag with [worker-review] prefix to distinguish from contractor ratings
                Rating.objects.create(
                    engagement=engagement,
                    contractor=engagement.contractor,
                    worker=engagement.worker,
                    score=score,
                    review=f'[worker-review] {review}',
                )
                messages.success(request, 'Rating submitted!')
                return redirect('/worker/my-jobs/')

        return render(request, 'shared/rate.html', {
            'engagement': engagement,
            'ratee': engagement.contractor,
            'is_contractor': False,
        })


@login_required
def submit_endorsement(request, engagement_id):
    """Only contractors can endorse workers after job completion."""
    if not request.user.is_contractor:
        return redirect('/')

    engagement = get_object_or_404(
        JobEngagement, id=engagement_id, contractor=request.user, status='completed'
    )

    if request.method == 'POST':
        tags = request.POST.getlist('tags')
        valid_tags = [tag for tag in ENDORSEMENT_TAGS]
        for tag in tags:
            if tag in valid_tags:
                SkillEndorsement.objects.get_or_create(
                    engagement=engagement,
                    contractor=request.user,
                    worker=engagement.worker,
                    skill_tag=tag,
                )
        messages.success(request, f'Endorsed {engagement.worker.name}!')
        return redirect('contractor_dashboard')

    existing_tags = list(SkillEndorsement.objects.filter(
        engagement=engagement
    ).values_list('skill_tag', flat=True))

    return render(request, 'shared/endorse.html', {
        'engagement': engagement,
        'endorsement_tags': ENDORSEMENT_TAGS,
        'existing_tags': existing_tags,
    })