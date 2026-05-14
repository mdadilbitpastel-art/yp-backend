"""Read-only list endpoints for the shared Data Management models.

These mirror what the dashboard manages under Data Management →
Statistics / Employers / Team Members / Social Media, so the frontend
can fetch the full catalogue independently of any specific page
section.  Rows already appear nested inside section endpoints (e.g.
/api/home/network/ for picked stats) — these endpoints return *all*
rows in canonical order.
"""

from rest_framework.generics import ListAPIView

from .models import Employer, SocialMediaIcon, Statistic, TeamMember
from .serializers import (
    EmployerSerializer,
    SocialMediaIconSerializer,
    StatisticSerializer,
    TeamMemberSerializer,
)


class StatisticListView(ListAPIView):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    pagination_class = None


class EmployerListView(ListAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    pagination_class = None


class TeamMemberListView(ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    pagination_class = None


class SocialMediaIconListView(ListAPIView):
    queryset = SocialMediaIcon.objects.all()
    serializer_class = SocialMediaIconSerializer
    pagination_class = None
