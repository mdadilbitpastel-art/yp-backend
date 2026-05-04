"""Public read-only API for the home app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from .models import (
    AboutSection,
    ApplySection,
    FeatureSection,
    HeroSection,
    NetworkSection,
    TalentPoolSection,
)
from .serializers import (
    AboutSectionSerializer,
    ApplySectionSerializer,
    FeatureSectionSerializer,
    HeroSectionSerializer,
    HomePageSerializer,
    NetworkSectionSerializer,
    TalentPoolSectionSerializer,
)


class _SingletonMixin:
    """Each subclass sets `singleton_model` to its singleton class."""

    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class ActiveHeroSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = HeroSection
    serializer_class = HeroSectionSerializer


class ActiveFeatureSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = FeatureSection
    serializer_class = FeatureSectionSerializer


class ActiveAboutSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AboutSection
    serializer_class = AboutSectionSerializer


class ActiveNetworkSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = NetworkSection
    serializer_class = NetworkSectionSerializer


class ActiveTalentPoolSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = TalentPoolSection
    serializer_class = TalentPoolSectionSerializer


class ActiveApplySectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = ApplySection
    serializer_class = ApplySectionSerializer


class HomePageView(_SingletonMixin, RetrieveAPIView):
    """Combined homepage payload — every section in one response."""

    singleton_model = HeroSection  # any singleton — serializer reloads each.
    serializer_class = HomePageSerializer
