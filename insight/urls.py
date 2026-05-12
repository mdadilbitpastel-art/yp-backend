"""Insight app API routes — mounted under /api/insight/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.InsightPageView.as_view(), name="api-insight"),
    path("hero/", views.InsightHeroSectionView.as_view(), name="api-insight-hero"),
    path("founder/", views.InsightFounderSectionView.as_view(), name="api-insight-founder"),
    path("article/", views.InsightArticleSectionView.as_view(), name="api-insight-article"),
    path("lane/", views.InsightLaneSectionView.as_view(), name="api-insight-lane"),
    path("subscribe/", views.InsightSubscribeSectionView.as_view(), name="api-insight-subscribe"),
]
