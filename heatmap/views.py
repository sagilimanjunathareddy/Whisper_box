from django.shortcuts import render
from stories.models import Story
import json
import logging

logger = logging.getLogger(__name__)

def map_view(request):
    """
    Prepare points list. Accept location formatted as 'lat,lng'.
    Returns JSON string for template.
    """
    points = []
    for s in Story.objects.exclude(location='').order_by('-created_at'):
        loc = s.location.strip()
        # Accept multiple formats: "lat,lng" or "lat, lng"
        try:
            lat_str, lng_str = loc.split(',')
            lat = float(lat_str.strip())
            lng = float(lng_str.strip())
            points.append({
                'id': s.id,
                'title': s.title or (s.category + " @ " + (s.city or "Unknown")),
                'category': s.category,
                'lat': lat,
                'lng': lng,
            })
        except Exception as e:
            # skip invalid values but log them for debugging
            logger.debug(f"Skipping Story id={s.id} due to invalid location: '{s.location}' -> {e}")

    # For debugging in development: pass a flag if no points found
    debug_empty = len(points) == 0

    # Optional: add an example point to help verify map works (remove for production)
    # Example coords: New Delhi
    if debug_empty:
        points = [
            {'id': 0, 'title': 'Example Unsafe Area (Delhi)', 'category': 'example', 'lat': 28.6139, 'lng': 77.2090}
        ]

    return render(request, 'heatmap/map.html', {
        'points_json': json.dumps(points),
        'has_real_points': not debug_empty,
    })
