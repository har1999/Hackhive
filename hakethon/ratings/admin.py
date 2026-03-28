from django.contrib import admin
from .models import Rating, SkillEndorsement

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rater', 'ratee', 'score', 'direction', 'created_at']
    list_filter = ['direction', 'score']
    search_fields = ['rater__name', 'ratee__name']
    readonly_fields = ['rater', 'ratee', 'engagement', 'score', 'note', 'direction', 'created_at']
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False

@admin.register(SkillEndorsement)
class EndorsementAdmin(admin.ModelAdmin):
    list_display = ['contractor', 'worker', 'tag', 'created_at']
    list_filter = ['tag']
    search_fields = ['contractor__name', 'worker__name']
