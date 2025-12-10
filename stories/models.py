# stories/models.py
from django.db import models
from django.utils import timezone
import os

class Story(models.Model):
    CATEGORY_CHOICES = [
        ("stalking", "Stalking"),
        ("eve_teasing", "Eve Teasing"),
        ("cyber", "Cyber Harassment"),
        ("workplace", "Workplace Harassment"),
        ("abuse", "Physical Abuse"),
    ]

    title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    city = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)  # optional 'lat,lng' for heatmap
    story_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} @ {self.city or 'Unknown'} - {self.created_at.date()}"


def evidence_upload_path(instance, filename):
    # store under media/evidence/story_<id>/timestamp_filename
    ts = timezone.now().strftime("%Y%m%d%H%M%S")
    safe_name = filename.replace(" ", "_")
    return f"evidence/story_{instance.story.id}/{ts}_{safe_name}"


class Evidence(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='evidence')
    file = models.FileField(upload_to=evidence_upload_path)
    thumbnail = models.ImageField(upload_to='evidence/thumbnails/', null=True, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # moderation flag, optional

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"Evidence for story {self.story.id} — {self.filename()}"
