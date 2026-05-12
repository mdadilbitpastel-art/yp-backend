"""DRF serializers for the employers app."""

from rest_framework import serializers

from data_management.models import section_images
from home.models import NetworkSection
from home.serializers import NetworkSectionSerializer

from .models import (
    EmployersEventsSection,
    EmployersHeroSection,
    EmployersMissionSection,
    EmployersOfferSection,
)


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


def _images_payload(section, request):
    return [_absolute_url(row["image"], request) for row in section_images(section)]


class EmployersHeroSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
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
            "images": _images_payload(instance, request),
        }


class EmployersMissionPointSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    text = serializers.CharField(allow_blank=True)


class EmployersMissionSectionSerializer(serializers.Serializer):
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
            "points": EmployersMissionPointSerializer(
                instance.mission_points(),
                many=True,
                context=self.context,
            ).data,
            "images": _images_payload(instance, request),
        }


class EmployersOfferCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    icon = serializers.SerializerMethodField()
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)

    def get_icon(self, obj):
        return _absolute_url(obj.get("icon"), self.context.get("request"))


class EmployersOfferSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "cards": EmployersOfferCardSerializer(
                instance.offer_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class EmployersEventImageSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _absolute_url(obj.get("image"), self.context.get("request"))


class EmployersEventsSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
            "images": EmployersEventImageSerializer(
                instance.event_images(),
                many=True,
                context=self.context,
            ).data,
        }


class EmployersPageSerializer(serializers.Serializer):
    """Combined Employers page payload — every section in one response.

    Note: network section shares the home NetworkSection singleton."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "hero": EmployersHeroSectionSerializer(EmployersHeroSection.load(), context=ctx).data,
            "network": NetworkSectionSerializer(NetworkSection.load(), context=ctx).data,
            "mission": EmployersMissionSectionSerializer(EmployersMissionSection.load(), context=ctx).data,
            "offer": EmployersOfferSectionSerializer(EmployersOfferSection.load(), context=ctx).data,
            "events": EmployersEventsSectionSerializer(EmployersEventsSection.load(), context=ctx).data,
        }
