"""Public read-only API for the home app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from .models import (
    AboutSection,
    AppSection,
    ApplySection,
    FeatureSection,
    FooterSettings,
    HeaderSettings,
    HeroSection,
    NetworkSection,
    SocialMediaSection,
    TalentPoolSection,
    TestimonialsSection,
)
from .serializers import (
    AboutSectionSerializer,
    AppSectionSerializer,
    ApplySectionSerializer,
    FeatureSectionSerializer,
    FooterSettingsSerializer,
    HeaderSettingsSerializer,
    HeroSectionSerializer,
    HomePageSerializer,
    NetworkSectionSerializer,
    SocialMediaSectionSerializer,
    TalentPoolSectionSerializer,
    TestimonialsSectionSerializer,
)


class _SingletonMixin:
    """Each subclass sets `singleton_model` to its singleton class."""

    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class ActiveHeaderView(_SingletonMixin, RetrieveAPIView):
    singleton_model = HeaderSettings
    serializer_class = HeaderSettingsSerializer


class ActiveFooterView(_SingletonMixin, RetrieveAPIView):
    singleton_model = FooterSettings
    serializer_class = FooterSettingsSerializer


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


class ActiveSocialMediaSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = SocialMediaSection
    serializer_class = SocialMediaSectionSerializer


class ActiveTestimonialsSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = TestimonialsSection
    serializer_class = TestimonialsSectionSerializer


class ActiveAppSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = AppSection
    serializer_class = AppSectionSerializer


class HomePageView(_SingletonMixin, RetrieveAPIView):
    """Combined homepage payload — every section in one response."""

    singleton_model = HeroSection  # any singleton — serializer reloads each.
    serializer_class = HomePageSerializer
