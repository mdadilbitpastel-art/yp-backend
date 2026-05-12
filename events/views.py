"""Public read-only API for the events app — consumed by the Next.js frontend."""

from rest_framework.generics import RetrieveAPIView

from .models import (
    EventsFeaturedSection,
    EventsHeroSection,
    EventsMissedSection,
    EventsSubmitSection,
    EventsUpcomingSection,
)
from .serializers import (
    EventsFeaturedSectionSerializer,
    EventsHeroSectionSerializer,
    EventsMissedSectionSerializer,
    EventsPageSerializer,
    EventsSubmitSectionSerializer,
    EventsUpcomingSectionSerializer,
)


class _SingletonMixin:
    singleton_model = None

    def get_object(self):
        return self.singleton_model.load()


class EventsHeroSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EventsHeroSection
    serializer_class = EventsHeroSectionSerializer


class EventsFeaturedSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EventsFeaturedSection
    serializer_class = EventsFeaturedSectionSerializer


class EventsUpcomingSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EventsUpcomingSection
    serializer_class = EventsUpcomingSectionSerializer


class EventsMissedSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EventsMissedSection
    serializer_class = EventsMissedSectionSerializer


class EventsSubmitSectionView(_SingletonMixin, RetrieveAPIView):
    singleton_model = EventsSubmitSection
    serializer_class = EventsSubmitSectionSerializer


class EventsPageView(_SingletonMixin, RetrieveAPIView):
    """Combined Events payload — every section in one response."""

    singleton_model = EventsHeroSection
    serializer_class = EventsPageSerializer
