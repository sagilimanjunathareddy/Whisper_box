# admin_dashboard/views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from stories.models import Story
from django.db.models import Count
from django.utils import timezone

@staff_member_required
def index(request):
    # Basic stats
    total_stories = Story.objects.count()

    # Recent 5 stories (most recent first)
    recent_stories = Story.objects.all().order_by('-created_at')[:5]

    # Category counts
    category_counts = Story.objects.values('category').annotate(count=Count('id')).order_by('-count')

    # Recent by day (last 7 days) sample for a tiny chart (list)
    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    recent_week = Story.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')[:10]

    context = {
        'total_stories': total_stories,
        'recent_stories': recent_stories,
        'category_counts': category_counts,
        'recent_week': recent_week,
    }
    return render(request, 'admin_dashboard/index.html', context)


@staff_member_required
def analytics(request):
    # More detailed analytics - placeholder
    category_counts = Story.objects.values('category').annotate(count=Count('id')).order_by('-count')
    by_city = Story.objects.values('city').annotate(count=Count('id')).order_by('-count')[:10]
    context = {
        'category_counts': category_counts,
        'by_city': by_city,
    }
    return render(request, 'admin_dashboard/analytics.html', context)
