"""DRF serializers for the schools app."""

from rest_framework import serializers

from data_management.models import section_images

from .models import (
    SchoolsBenchmarkSection,
    SchoolsEmployerSection,
    SchoolsFaqSection,
    SchoolsHelpSection,
    SchoolsHeroSection,
    SchoolsSubscribeSection,
)


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


def _images_payload(section, request):
    return [_absolute_url(row["image"], request) for row in section_images(section)]


class SchoolsHeroSectionSerializer(serializers.Serializer):
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


class SchoolsHelpCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)


class SchoolsHelpSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "cards": SchoolsHelpCardSerializer(
                instance.help_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class SchoolsEmployerLogoSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return _absolute_url(obj.get("logo"), self.context.get("request"))


class SchoolsEmployerSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
            "employers": SchoolsEmployerLogoSerializer(
                instance.employers(),
                many=True,
                context=self.context,
            ).data,
        }


class SchoolsBenchmarkCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)


class SchoolsBenchmarkSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "cards": SchoolsBenchmarkCardSerializer(
                instance.benchmark_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class SchoolsSubscribeFieldSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    field_name = serializers.CharField(allow_blank=True)
    placeholder = serializers.CharField(allow_blank=True)


class SchoolsSubscribeSectionSerializer(serializers.Serializer):
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
            "fields": SchoolsSubscribeFieldSerializer(
                instance.subscribe_fields(),
                many=True,
                context=self.context,
            ).data,
            "images": _images_payload(instance, request),
        }


class SchoolsFaqItemSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    question = serializers.CharField(allow_blank=True)
    answer = serializers.CharField(allow_blank=True)


class SchoolsFaqSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "items": SchoolsFaqItemSerializer(
                instance.faq_items(),
                many=True,
                context=self.context,
            ).data,
        }


class SchoolsPageSerializer(serializers.Serializer):
    """Combined Schools page payload — every section in one response."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "hero": SchoolsHeroSectionSerializer(SchoolsHeroSection.load(), context=ctx).data,
            "help": SchoolsHelpSectionSerializer(SchoolsHelpSection.load(), context=ctx).data,
            "employer": SchoolsEmployerSectionSerializer(SchoolsEmployerSection.load(), context=ctx).data,
            "benchmark": SchoolsBenchmarkSectionSerializer(SchoolsBenchmarkSection.load(), context=ctx).data,
            "subscribe": SchoolsSubscribeSectionSerializer(SchoolsSubscribeSection.load(), context=ctx).data,
            "faq": SchoolsFaqSectionSerializer(SchoolsFaqSection.load(), context=ctx).data,
        }
