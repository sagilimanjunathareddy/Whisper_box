# stories/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponseForbidden
from .models import Story, Evidence
from .forms import StoryForm

# image handling
from PIL import Image
from django.core.files.base import ContentFile
import io, os

# Optional: requests for server-side geocoding if you use it elsewhere
# import requests

# Helper: safe file processing and thumbnail creation
def handle_uploaded_file(story, uploaded_file):
    """
    Validate, sanitize and save uploaded_file as Evidence for `story`.
    Returns (Evidence instance, error_message_or_None)
    """
    # basic checks
    MAX_SIZE = getattr(settings, "MAX_UPLOAD_SIZE", 5 * 1024 * 1024)
    ALLOWED = getattr(settings, "ALLOWED_UPLOAD_CONTENT_TYPES", [
        "image/jpeg", "image/png", "image/webp", "application/pdf"
    ])

    size = uploaded_file.size
    ctype = uploaded_file.content_type or ''

    if size > MAX_SIZE:
        return None, "File too large"

    if ctype not in ALLOWED:
        return None, "Invalid file type"

    # create Evidence instance (don't save yet)
    evid = Evidence(story=story, content_type=ctype, size=size)
    evid.file.save(uploaded_file.name, uploaded_file, save=False)

    # If it's an image, sanitize and create thumbnail
    if ctype.startswith("image/"):
        try:
            evid.file.seek(0)
            img = Image.open(evid.file)

            # Normalize image mode
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Strip EXIF by re-saving image data to a new Image
            data = list(img.getdata())
            sanitized = Image.new(img.mode, img.size)
            sanitized.putdata(data)

            # Optionally resize original to a max size to save space
            max_size = (1600, 1600)
            sanitized.thumbnail(max_size, Image.ANTIALIAS)

            # Save sanitized original to buffer
            buf = io.BytesIO()
            sanitized.save(buf, format="JPEG", quality=85)
            buf.seek(0)
            evid.file.save(evid.file.name, ContentFile(buf.read()), save=False)

            # Create thumbnail  (320x320)
            thumb = sanitized.copy()
            thumb.thumbnail((320, 320), Image.ANTIALIAS)
            buf_thumb = io.BytesIO()
            thumb.save(buf_thumb, format="JPEG", quality=75)
            buf_thumb.seek(0)
            thumb_name = f"thumb_{os.path.basename(evid.file.name)}"
            evid.thumbnail.save(thumb_name, ContentFile(buf_thumb.read()), save=False)
        except Exception as e:
            # if image processing fails, continue without thumbnail
            print("Image processing error:", e)

    # Save evidence record
    evid.save()
    return evid, None


# Views
def story_list(request):
    q = request.GET.get('q')
    stories = Story.objects.all().order_by('-created_at')
    if q:
        stories = stories.filter(description__icontains=q)

    paginator = Paginator(stories, 6)
    page = request.GET.get('page')
    stories_page = paginator.get_page(page)

    return render(request, 'stories/story_list.html', {'stories': stories_page})


def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    # show only approved evidence for public; admins see all (optional)
    evidence_qs = story.evidence.all()
    # if you want admins to see unapproved, you can adjust logic

    return render(request, 'stories/story_detail.html', {
        'story': story,
        'evidence_list': evidence_qs,
    })


def submit_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)

            # Optional: you can include geocoding logic here (server-side) as earlier discussed
            # e.g., if not story.location and story.city: geocode and set story.location

            story.save()

            # Process uploaded files (multiple)
            files = request.FILES.getlist('evidence_files')
            for f in files:
                evid, err = handle_uploaded_file(story, f)
                if err:
                    # Optionally capture error messages for user: e.g., messages.warning(request, err)
                    print("Upload error:", err)
            return redirect('stories:story_list')
    else:
        form = StoryForm()
    return render(request, 'stories/submit_story.html', {'form': form})
