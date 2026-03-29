from django.contrib import admin
from .models import Rating, SkillEndorsement

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['contractor', 'worker', 'score', 'engagement', 'created_at']
    list_filter = ['score']
    readonly_fields = ['engagement', 'contractor', 'worker', 'score', 'review']
    search_fields = ['contractor__name', 'worker__name', 'review']

@admin.register(SkillEndorsement)
class EndorsementAdmin(admin.ModelAdmin):
    list_display = ['contractor', 'worker', 'skill_tag', 'engagement', 'created_at']
    list_filter = ['skill_tag']
    readonly_fields = ['engagement', 'contractor', 'worker', 'skill_tag']
    search_fields = ['contractor__name', 'worker__name', 'skill_tag']