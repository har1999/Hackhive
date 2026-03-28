from django.contrib import admin

from .models import (
    ContractorProfile,
    FavoriteWorker,
    JobApplication,
    JobEngagement,
    JobPosting,
    SkillEndorsement,
    WorkerProfile,
)


@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_skill', 'location', 'phone_number')
    search_fields = ('name', 'phone_number', 'location')


@admin.register(ContractorProfile)
class ContractorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number')
    search_fields = ('name', 'phone_number')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill_required', 'location', 'daily_rate', 'status', 'urgent_same_day')
    list_filter = ('skill_required', 'status', 'urgent_same_day')
    search_fields = ('title', 'location')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'worker', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(JobEngagement)
class JobEngagementAdmin(admin.ModelAdmin):
    list_display = ('job', 'worker', 'contractor', 'contractor_rating_for_worker', 'worker_rating_for_contractor')


@admin.register(SkillEndorsement)
class SkillEndorsementAdmin(admin.ModelAdmin):
    list_display = ('engagement', 'skill_tag')


@admin.register(FavoriteWorker)
class FavoriteWorkerAdmin(admin.ModelAdmin):
    list_display = ('contractor', 'worker', 'created_at')
