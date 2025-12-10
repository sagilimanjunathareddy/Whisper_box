from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Redirect home → stories list
    path('', RedirectView.as_view(url='/stories/')),

    # App URLs
    path('stories/', include('stories.urls')),
    path('comments/', include('comments.urls')),
    path('heatmap/', include('heatmap.urls')),
    path('dashboard/', include('admin_dashboard.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
