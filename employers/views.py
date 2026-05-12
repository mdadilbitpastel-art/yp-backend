"""Public read-only API for the employers app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from home.models import NetworkSection
from home.serializers import NetworkSectionSerializer

from .models import (
    EmployersEventsSection,
    EmployersHeroSection,
    EmployersMissionSection,
    EmployersOfferSection,
)
from .serializers import (
    EmployersEventsSectionSerializer,
    EmployersHeroSectionSerializer,
    EmployersMissionSectionSerializer,
    EmployersOfferSectionSerializer,
    EmployersPageSerializer,
)


class _SingletonMixin:
    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class EmployersHeroSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EmployersHeroSection
    serializer_class = EmployersHeroSectionSerializer


class EmployersMissionSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EmployersMissionSection
    serializer_class = EmployersMissionSectionSerializer


class EmployersOfferSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EmployersOfferSection
    serializer_class = EmployersOfferSectionSerializer


class EmployersEventsSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EmployersEventsSection
    serializer_class = EmployersEventsSectionSerializer


class EmployersNetworkSectionView(_SingletonMixin, RetrieveAPIView):
    """Employers reuses the shared NetworkSection singleton."""

    singleton_model = NetworkSection
    serializer_class = NetworkSectionSerializer


class EmployersPageView(_SingletonMixin, RetrieveAPIView):
    """Combined Employers payload — every section in one response."""

    singleton_model = EmployersHeroSection
    serializer_class = EmployersPageSerializer
