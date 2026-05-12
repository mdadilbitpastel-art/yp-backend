"""Public read-only API for the insight app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from .models import (
    InsightArticleSection,
    InsightFounderSection,
    InsightHeroSection,
    InsightLaneSection,
    InsightSubscribeSection,
)
from .serializers import (
    InsightArticleSectionSerializer,
    InsightFounderSectionSerializer,
    InsightHeroSectionSerializer,
    InsightLaneSectionSerializer,
    InsightPageSerializer,
    InsightSubscribeSectionSerializer,
)


class _SingletonMixin:
    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class InsightHeroSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = InsightHeroSection
    serializer_class = InsightHeroSectionSerializer


class InsightFounderSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = InsightFounderSection
    serializer_class = InsightFounderSectionSerializer


class InsightArticleSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = InsightArticleSection
    serializer_class = InsightArticleSectionSerializer


class InsightLaneSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = InsightLaneSection
    serializer_class = InsightLaneSectionSerializer


class InsightSubscribeSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = InsightSubscribeSection
    serializer_class = InsightSubscribeSectionSerializer


class InsightPageView(_SingletonMixin, RetrieveAPIView):
    """Combined Insight payload — every section in one response."""

    singleton_model = InsightHeroSection
    serializer_class = InsightPageSerializer
