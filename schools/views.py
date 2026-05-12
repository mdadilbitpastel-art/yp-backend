"""Public read-only API for the schools app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from .models import (
    SchoolsBenchmarkSection,
    SchoolsEmployerSection,
    SchoolsFaqSection,
    SchoolsHelpSection,
    SchoolsHeroSection,
    SchoolsSubscribeSection,
)
from .serializers import (
    SchoolsBenchmarkSectionSerializer,
    SchoolsEmployerSectionSerializer,
    SchoolsFaqSectionSerializer,
    SchoolsHelpSectionSerializer,
    SchoolsHeroSectionSerializer,
    SchoolsPageSerializer,
    SchoolsSubscribeSectionSerializer,
)


class _SingletonMixin:
    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class SchoolsHeroSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = SchoolsHeroSection
    serializer_class = SchoolsHeroSectionSerializer


class SchoolsHelpSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = SchoolsHelpSection
    serializer_class = SchoolsHelpSectionSerializer


class SchoolsEmployerSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = SchoolsEmployerSection
    serializer_class = SchoolsEmployerSectionSerializer


class SchoolsBenchmarkSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = SchoolsBenchmarkSection
    serializer_class = SchoolsBenchmarkSectionSerializer


class SchoolsSubscribeSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = SchoolsSubscribeSection
    serializer_class = SchoolsSubscribeSectionSerializer


class SchoolsFaqSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = SchoolsFaqSection
    serializer_class = SchoolsFaqSectionSerializer


class SchoolsPageView(_SingletonMixin, RetrieveAPIView):
    """Combined Schools payload — every section in one response."""

    singleton_model = SchoolsHeroSection
    serializer_class = SchoolsPageSerializer
