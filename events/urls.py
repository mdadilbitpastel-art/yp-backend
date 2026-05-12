"""Events app API routes — mounted under /api/events/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventsPageView.as_view(), name="api-events"),
    path("hero/", views.EventsHeroSectionView.as_view(), name="api-events-hero"),
    path("featured/", views.EventsFeaturedSectionView.as_view(), name="api-events-featured"),
    path("upcoming/", views.EventsUpcomingSectionView.as_view(), name="api-events-upcoming"),
    path("missed/", views.EventsMissedSectionView.as_view(), name="api-events-missed"),
    path("submit/", views.EventsSubmitSectionView.as_view(), name="api-events-submit"),
]
