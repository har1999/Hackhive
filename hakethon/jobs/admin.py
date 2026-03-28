from django.contrib import admin
from django.db.models import Count
from .models import Job, JobApplication, JobEngagement, PhotoEvidence

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'skill_category', 'contractor', 'location_name', 'daily_rate', 'status', 'is_urgent', 'app_count', 'created_at']
    list_filter = ['status', 'skill_category', 'is_urgent']
    search_fields = ['title', 'location_name', 'contractor__name']
    readonly_fields = ['created_at', 'updated_at']
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(app_count=Count('applications'))
    def app_count(self, obj): return obj.app_count
    app_count.short_description = 'Applications'

@admin.register(JobApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['worker', 'job', 'status', 'applied_at']
    list_filter = ['status']
    search_fields = ['worker__name', 'job__title']

@admin.register(JobEngagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ['worker', 'contractor', 'job', 'status', 'started_at', 'completed_at']
    list_filter = ['status']
    search_fields = ['worker__name', 'contractor__name', 'job__title']
    readonly_fields = ['started_at']
