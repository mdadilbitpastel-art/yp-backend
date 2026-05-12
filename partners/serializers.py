"""DRF serializers for the partners app."""

from rest_framework import serializers

from data_management.models import section_images

from .models import (
    PartnersFamilySection,
    PartnersFounderSection,
    PartnersHeroSection,
    PartnersPartnerSection,
    PartnersReviewSection,
)


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


def _images_payload(section, request):
    return [_absolute_url(row["image"], request) for row in section_images(section)]


class PartnersHeroSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "stats": instance.hero_stats(),
        }


class PartnersCategorySerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)


class PartnersEmployerSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    logo = serializers.SerializerMethodField()
    description = serializers.CharField(allow_blank=True)
    url = serializers.URLField(allow_blank=True)

    def get_logo(self, obj):
        return _absolute_url(obj.get("logo"), self.context.get("request"))


class PartnersPartnerSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "search_placeholder": instance.search_placeholder,
            "explore_button_text": instance.explore_button_text,
            "categories": PartnersCategorySerializer(
                instance.categories(),
                many=True,
                context=self.context,
            ).data,
            "employers": PartnersEmployerSerializer(
                instance.partner_employers(),
                many=True,
                context=self.context,
            ).data,
        }


class PartnersFamilySectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "employers": PartnersEmployerSerializer(
                instance.family_employers(),
                many=True,
                context=self.context,
            ).data,
            "load_more_button": {
                "text": instance.load_more_button_text,
                "url": instance.load_more_button_url,
            },
        }


class PartnersReviewCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    designation = serializers.CharField(allow_blank=True)
    message = serializers.CharField(allow_blank=True)


class PartnersReviewSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "cards": PartnersReviewCardSerializer(
                instance.review_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class PartnersFounderSectionSerializer(serializers.Serializer):
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


class PartnersPageSerializer(serializers.Serializer):
    """Combined Partners page payload — every section in one response."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "hero": PartnersHeroSectionSerializer(PartnersHeroSection.load(), context=ctx).data,
            "partner": PartnersPartnerSectionSerializer(PartnersPartnerSection.load(), context=ctx).data,
            "family": PartnersFamilySectionSerializer(PartnersFamilySection.load(), context=ctx).data,
            "review": PartnersReviewSectionSerializer(PartnersReviewSection.load(), context=ctx).data,
            "founder": PartnersFounderSectionSerializer(PartnersFounderSection.load(), context=ctx).data,
        }
