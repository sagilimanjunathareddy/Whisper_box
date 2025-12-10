from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from stories.models import Story
from .models import Comment

@require_POST
def add_comment(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    text = request.POST.get('text', '').strip()
    if text:
        # Basic profanity filter placeholder (extend with real moderation)
        banned = ['badword1', 'badword2']
        if any(b in text.lower() for b in banned):
            return redirect('stories:story_detail', pk=story.id)
        Comment.objects.create(story=story, text=text)
    return redirect('stories:story_detail', pk=story.id)
