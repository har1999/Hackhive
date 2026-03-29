from django.contrib import admin
from .models import ContractorProfile


@admin.register(ContractorProfile)
class ContractorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'location_name', 'total_jobs_display', 'avg_rating_display']
    search_fields = ['user__name', 'company_name']

    def total_jobs_display(self, obj):
        return obj.total_jobs_posted
    total_jobs_display.short_description = 'Jobs Posted'

    def avg_rating_display(self, obj):
        return obj.average_rating
    avg_rating_display.short_description = 'Avg Rating'