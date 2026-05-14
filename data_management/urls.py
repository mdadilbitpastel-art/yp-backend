"""Data Management app API routes — mounted under /api/data/."""

from django.urls import path

from . import views

urlpatterns = [
    path("statistics/", views.StatisticListView.as_view(), name="api-data-statistics"),
    path("employers/", views.EmployerListView.as_view(), name="api-data-employers"),
    path("team-members/", views.TeamMemberListView.as_view(), name="api-data-team-members"),
    path("social-media/", views.SocialMediaIconListView.as_view(), name="api-data-social-media"),
]
