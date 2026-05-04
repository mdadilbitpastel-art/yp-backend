"""Home app API routes — mounted under /api/home/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="api-home"),
    path("hero/", views.ActiveHeroSectionView.as_view(), name="api-hero"),
    path("features/", views.ActiveFeatureSectionView.as_view(), name="api-features"),
    path("about/", views.ActiveAboutSectionView.as_view(), name="api-about"),
    path("network/", views.ActiveNetworkSectionView.as_view(), name="api-network"),
    path("talent-pool/", views.ActiveTalentPoolSectionView.as_view(), name="api-talent-pool"),
    path("apply/", views.ActiveApplySectionView.as_view(), name="api-apply"),
]
