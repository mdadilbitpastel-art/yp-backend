"""Employers app API routes — mounted under /api/employers/."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.EmployersPageView.as_view(), name="api-employers"),
    path("hero/", views.EmployersHeroSectionView.as_view(), name="api-employers-hero"),
    path("network/", views.EmployersNetworkSectionView.as_view(), name="api-employers-network"),
    path("mission/", views.EmployersMissionSectionView.as_view(), name="api-employers-mission"),
    path("offer/", views.EmployersOfferSectionView.as_view(), name="api-employers-offer"),
    path("events/", views.EmployersEventsSectionView.as_view(), name="api-employers-events"),
]
