from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import WorkerProfile
from jobs.models import SKILL_CHOICES

@login_required
def worker_setup(request):
    profile, _ = WorkerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.skill_category = request.POST.get('skill_category', '')
        profile.location_name = request.POST.get('location_name', '')
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        if lat: profile.latitude = float(lat)
        if lng: profile.longitude = float(lng)
        profile.preferred_radius_km = int(request.POST.get('radius', 15))
        profile.save()
        return redirect('/worker/feed/')
    return render(request, 'worker/setup.html', {'profile': profile, 'skill_choices': SKILL_CHOICES})
