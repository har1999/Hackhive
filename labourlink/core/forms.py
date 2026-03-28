from django import forms

from .models import (
    ContractorProfile,
    FavoriteWorker,
    JobEngagement,
    JobPosting,
    SkillEndorsement,
    WorkerProfile,
)


class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ['name', 'location', 'phone_number', 'primary_skill']


class ContractorProfileForm(forms.ModelForm):
    class Meta:
        model = ContractorProfile
        fields = ['name', 'location', 'phone_number']


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title',
            'skill_required',
            'location',
            'duration_days',
            'daily_rate',
            'workers_needed',
            'radius_km',
            'urgent_same_day',
            'start_date',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


class JobApplyForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=WorkerProfile.objects.none())

    def __init__(self, *args, **kwargs):
        skill = kwargs.pop('skill', None)
        super().__init__(*args, **kwargs)
        queryset = WorkerProfile.objects.all().order_by('name')
        if skill:
            queryset = queryset.filter(primary_skill=skill)
        self.fields['worker'].queryset = queryset


class EngagementRatingForm(forms.ModelForm):
    endorsement_1 = forms.CharField(max_length=80, required=False)
    endorsement_2 = forms.CharField(max_length=80, required=False)

    class Meta:
        model = JobEngagement
        fields = [
            'worker',
            'completed_on',
            'contractor_rating_for_worker',
            'worker_rating_for_contractor',
            'note_for_worker',
            'note_for_contractor',
        ]
        widgets = {
            'completed_on': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        contractor = kwargs.pop('contractor', None)
        super().__init__(*args, **kwargs)
        if contractor is not None:
            self.fields['worker'].queryset = WorkerProfile.objects.filter(
                applications__job__contractor=contractor,
                applications__status='ACCEPTED',
            ).distinct()

    def save_endorsements(self, engagement):
        for field_name in ['endorsement_1', 'endorsement_2']:
            value = self.cleaned_data.get(field_name, '').strip()
            if value:
                SkillEndorsement.objects.create(engagement=engagement, skill_tag=value)


class FavoriteWorkerForm(forms.ModelForm):
    class Meta:
        model = FavoriteWorker
        fields = ['worker']
