"""Public read-only API for the partners app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from .models import (
    PartnersFamilySection,
    PartnersFounderSection,
    PartnersHeroSection,
    PartnersPartnerSection,
    PartnersReviewSection,
)
from .serializers import (
    PartnersFamilySectionSerializer,
    PartnersFounderSectionSerializer,
    PartnersHeroSectionSerializer,
    PartnersPageSerializer,
    PartnersPartnerSectionSerializer,
    PartnersReviewSectionSerializer,
)


class _SingletonMixin:
    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class PartnersHeroSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = PartnersHeroSection
    serializer_class = PartnersHeroSectionSerializer


class PartnersPartnerSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = PartnersPartnerSection
    serializer_class = PartnersPartnerSectionSerializer


class PartnersFamilySectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = PartnersFamilySection
    serializer_class = PartnersFamilySectionSerializer


class PartnersReviewSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = PartnersReviewSection
    serializer_class = PartnersReviewSectionSerializer


class PartnersFounderSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = PartnersFounderSection
    serializer_class = PartnersFounderSectionSerializer


class PartnersPageView(_SingletonMixin, RetrieveAPIView):
    """Combined Partners payload — every section in one response."""

    singleton_model = PartnersHeroSection
    serializer_class = PartnersPageSerializer
