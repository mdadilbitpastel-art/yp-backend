"""URL configuration for young_professionals.

Custom CMS dashboard at /dashboard/ + headless API at /api/home/.
Django Admin is intentionally not mounted.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard:index", permanent=False)),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("api/home/", include("home.urls")),
    path("api/about-us/", include("about_us.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
