"""Home app API routes — mounted under /api/home/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="api-home"),
    path("header/", views.ActiveHeaderView.as_view(), name="api-home-header"),
    path("footer/", views.ActiveFooterView.as_view(), name="api-home-footer"),
    path("hero/", views.ActiveHeroSectionView.as_view(), name="api-home-hero"),
    path("features/", views.ActiveFeatureSectionView.as_view(), name="api-home-features"),
    path("about/", views.ActiveAboutSectionView.as_view(), name="api-home-about"),
    path("network/", views.ActiveNetworkSectionView.as_view(), name="api-home-network"),
    path("talent-pool/", views.ActiveTalentPoolSectionView.as_view(), name="api-home-talent-pool"),
    path("apply/", views.ActiveApplySectionView.as_view(), name="api-home-apply"),
    path("social-media/", views.ActiveSocialMediaSectionView.as_view(), name="api-home-social-media"),
    path("testimonials/", views.ActiveTestimonialsSectionView.as_view(), name="api-home-testimonials"),
    path("app/", views.ActiveAppSectionView.as_view(), name="api-home-app"),
]
