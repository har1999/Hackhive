"""
Ratings Views - KaamSetu
Submit ratings and endorsements after job completion.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Rating, SkillEndorsement, ENDORSEMENT_TAGS
from jobs.models import JobEngagement


@login_required
def submit_rating(request, engagement_id):
    engagement = get_object_or_404(JobEngagement, id=engagement_id, status='completed')

    # Verify user is part of this engagement
    if request.user not in [engagement.worker, engagement.contractor]:
        messages.error(request, 'Not authorized')
        return redirect('/')

    if request.user == engagement.worker:
        direction = 'worker_to_contractor'
        ratee = engagement.contractor
    else:
        direction = 'contractor_to_worker'
        ratee = engagement.worker

    # Check if already rated
    if Rating.objects.filter(engagement=engagement, direction=direction).exists():
        messages.info(request, 'You have already rated this engagement.')
        if request.user.is_contractor:
            return redirect(f'/contractor/endorse/{engagement_id}/')
        return redirect('/worker/my-jobs/')

    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        note = request.POST.get('note', '')[:280]

        if not 1 <= score <= 5:
            messages.error(request, 'Score must be between 1 and 5')
        else:
            Rating.objects.create(
                engagement=engagement,
                rater=request.user,
                ratee=ratee,
                direction=direction,
                score=score,
                note=note,
            )
            messages.success(request, 'Rating submitted! Thank you.')
            if request.user.is_contractor:
                return redirect(f'/contractor/endorse/{engagement_id}/')
            return redirect('/worker/my-jobs/')

    return render(request, 'shared/rate.html', {
        'engagement': engagement,
        'ratee': ratee,
        'direction': direction,
    })


@login_required
def submit_endorsement(request, engagement_id):
    """Only contractors can endorse. After rating only."""
    if not request.user.is_contractor:
        return redirect('/')

    engagement = get_object_or_404(
        JobEngagement, id=engagement_id, contractor=request.user, status='completed'
    )

    if request.method == 'POST':
        tags = request.POST.getlist('tags')
        for tag in tags:
            if tag in dict(ENDORSEMENT_TAGS):
                SkillEndorsement.objects.get_or_create(
                    engagement=engagement,
                    contractor=request.user,
                    worker=engagement.worker,
                    tag=tag,
                )
        messages.success(request, f'Endorsed {engagement.worker.name}!')
        return redirect('/contractor/dashboard/')

    existing_tags = SkillEndorsement.objects.filter(
        engagement=engagement
    ).values_list('tag', flat=True)

    return render(request, 'shared/endorse.html', {
        'engagement': engagement,
        'endorsement_tags': ENDORSEMENT_TAGS,
        'existing_tags': list(existing_tags),
    })
