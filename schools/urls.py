"""Schools app API routes — mounted under /api/schools/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.SchoolsPageView.as_view(), name="api-schools"),
    path("hero/", views.SchoolsHeroSectionView.as_view(), name="api-schools-hero"),
    path("help/", views.SchoolsHelpSectionView.as_view(), name="api-schools-help"),
    path("employer/", views.SchoolsEmployerSectionView.as_view(), name="api-schools-employer"),
    path("benchmark/", views.SchoolsBenchmarkSectionView.as_view(), name="api-schools-benchmark"),
    path("subscribe/", views.SchoolsSubscribeSectionView.as_view(), name="api-schools-subscribe"),
    path("faq/", views.SchoolsFaqSectionView.as_view(), name="api-schools-faq"),
]
