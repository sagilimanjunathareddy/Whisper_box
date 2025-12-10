# stories/admin.py
from django.contrib import admin
from .models import Story, Evidence

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','city','story_date','created_at')
    search_fields = ('title','description','city','category')

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('id','story','filename','content_type','size','uploaded_at','is_approved')
    list_filter = ('content_type','is_approved')
    search_fields = ('file','story__description')
    actions = ['approve_evidence']

    def approve_evidence(self, request, queryset):
        queryset.update(is_approved=True)
    approve_evidence.short_description = "Approve selected evidence"
