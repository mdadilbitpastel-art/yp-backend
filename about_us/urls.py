"""About Us app API routes — mounted under /api/about-us/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.AboutUsPageView.as_view(), name="api-about-us"),
    path("hero/", views.AboutUsHeroSectionView.as_view(), name="api-about-us-hero"),
    path("mission/", views.AboutUsMissionSectionView.as_view(), name="api-about-us-mission"),
    path("founder/", views.AboutUsFounderSectionView.as_view(), name="api-about-us-founder"),
    path("values/", views.AboutUsValuesSectionView.as_view(), name="api-about-us-values"),
    path("journey/", views.AboutUsJourneySectionView.as_view(), name="api-about-us-journey"),
    path("pledge/", views.AboutUsPledgeSectionView.as_view(), name="api-about-us-pledge"),
    path("team/", views.AboutUsTeamSectionView.as_view(), name="api-about-us-team"),
    path("community/", views.AboutUsCommunitySectionView.as_view(), name="api-about-us-community"),
    path("social-media/", views.AboutUsSocialMediaSectionView.as_view(), name="api-about-us-social-media"),
]
