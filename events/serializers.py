"""DRF serializers for the events app."""

from rest_framework import serializers

from data_management.models import section_images

from .models import (
    EventsFeaturedSection,
    EventsHeroSection,
    EventsMissedSection,
    EventsSubmitSection,
    EventsUpcomingSection,
)


def _absolute_url(file_field, request):
    if not file_field:
        return None
    return request.build_absolute_uri(file_field.url) if request else file_field.url


def _images_payload(section, request):
    return [_absolute_url(row["image"], request) for row in section_images(section)]


class EventsHeroSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "primary_button": {
                "text": instance.primary_button_text,
                "url": instance.primary_button_url,
            },
            "secondary_button": {
                "text": instance.secondary_button_text,
                "url": instance.secondary_button_url,
            },
        }


class EventsFeaturedSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.label,
            "datetime_label": instance.datetime_label,
            "title": instance.title,
            "description": instance.description,
            "category_label": instance.category_label,
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
            "images": _images_payload(instance, request),
        }


class EventsUpcomingCategorySerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)


class EventsUpcomingCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    image = serializers.SerializerMethodField()
    label = serializers.CharField(allow_blank=True)
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    years_label = serializers.CharField(allow_blank=True)
    price_label = serializers.CharField(allow_blank=True)
    button_url = serializers.URLField(allow_blank=True)

    def get_image(self, obj):
        return _absolute_url(obj.get("image"), self.context.get("request"))


class EventsUpcomingSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "card_button_text": instance.card_button_text,
            "categories": EventsUpcomingCategorySerializer(
                instance.categories(),
                many=True,
                context=self.context,
            ).data,
            "cards": EventsUpcomingCardSerializer(
                instance.cards(),
                many=True,
                context=self.context,
            ).data,
        }


class EventsMissedCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    video = serializers.SerializerMethodField()
    title = serializers.CharField(allow_blank=True)
    date_label = serializers.CharField(allow_blank=True)
    button_url = serializers.URLField(allow_blank=True)

    def get_video(self, obj):
        return _absolute_url(obj.get("video"), self.context.get("request"))


class EventsMissedSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "card_button_text": instance.card_button_text,
            "cards": EventsMissedCardSerializer(
                instance.cards(),
                many=True,
                context=self.context,
            ).data,
        }


class EventsSubmitSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
            "images": _images_payload(instance, request),
        }


class EventsPageSerializer(serializers.Serializer):
    """Combined Events page payload — every section in one response."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "hero": EventsHeroSectionSerializer(EventsHeroSection.load(), context=ctx).data,
            "featured": EventsFeaturedSectionSerializer(EventsFeaturedSection.load(), context=ctx).data,
            "upcoming": EventsUpcomingSectionSerializer(EventsUpcomingSection.load(), context=ctx).data,
            "missed": EventsMissedSectionSerializer(EventsMissedSection.load(), context=ctx).data,
            "submit": EventsSubmitSectionSerializer(EventsSubmitSection.load(), context=ctx).data,
        }
