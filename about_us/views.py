"""Public read-only API for the about_us app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from .models import (
    AboutUsCommunitySection,
    AboutUsFounderSection,
    AboutUsHeroSection,
    AboutUsJourneySection,
    AboutUsMissionSection,
    AboutUsPledgeSection,
    AboutUsTeamSection,
    AboutUsValuesSection,
)
from .serializers import (
    AboutUsCommunitySectionSerializer,
    AboutUsFounderSectionSerializer,
    AboutUsHeroSectionSerializer,
    AboutUsJourneySectionSerializer,
    AboutUsMissionSectionSerializer,
    AboutUsPledgeSectionSerializer,
    AboutUsTeamSectionSerializer,
    AboutUsValuesSectionSerializer,
)


class _SingletonMixin:
    """Each subclass sets `singleton_model` to its singleton class."""

    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class AboutUsHeroSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsHeroSection
    serializer_class = AboutUsHeroSectionSerializer


class AboutUsMissionSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsMissionSection
    serializer_class = AboutUsMissionSectionSerializer


class AboutUsFounderSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsFounderSection
    serializer_class = AboutUsFounderSectionSerializer


class AboutUsValuesSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsValuesSection
    serializer_class = AboutUsValuesSectionSerializer


class AboutUsJourneySectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsJourneySection
    serializer_class = AboutUsJourneySectionSerializer


class AboutUsPledgeSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsPledgeSection
    serializer_class = AboutUsPledgeSectionSerializer


class AboutUsTeamSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsTeamSection
    serializer_class = AboutUsTeamSectionSerializer


class AboutUsCommunitySectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutUsCommunitySection
    serializer_class = AboutUsCommunitySectionSerializer
