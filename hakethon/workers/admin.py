from django.contrib import admin
from .models import WorkerProfile, FavouriteWorker

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_category', 'location_name', 'is_available', 'trust_level_display']
    list_filter = ['skill_category', 'is_available']
    search_fields = ['user__name', 'user__phone', 'location_name']
    def trust_level_display(self, obj): return obj.trust_level
    trust_level_display.short_description = 'Trust Level'

@admin.register(FavouriteWorker)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['contractor', 'worker', 'added_at']
