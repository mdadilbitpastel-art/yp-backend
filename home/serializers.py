"""DRF serializers for the home app."""

from rest_framework import serializers

from .models import (
    AboutSection,
    ApplySection,
    FeatureSection,
    HeroSection,
    NetworkSection,
    TalentPoolSection,
)


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = [
            "id",
            "title",
            "description",
            "highlight_text",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
            "background_image",
            "hero_image",
        ]


class FeatureCardSerializer(serializers.Serializer):
    """Single feature card — built from `FeatureSection.feature_cards()` dicts."""

    position = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    icon = serializers.SerializerMethodField()
    button_url = serializers.URLField(allow_blank=True)

    def get_icon(self, obj):
        return _absolute_url(obj.get("icon"), self.context.get("request"))


class FeatureSectionSerializer(serializers.ModelSerializer):
    """Feature section — title/description plus the active cards as a list."""

    class Meta:
        model = FeatureSection
        fields = ["features_title", "features_description"]

    def to_representation(self, instance):
        return {
            "title": instance.features_title,
            "description": instance.features_description,
            "button_text": instance.features_button_text,
            "cards": FeatureCardSerializer(
                instance.feature_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class AboutSectionSerializer(serializers.Serializer):
    """About / Mission section — flat fields with structured button payloads."""

    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.about_section_label,
            "title": instance.about_section_title,
            "description": instance.about_section_description,
            "image": _absolute_url(instance.about_section_image, request),
            "primary_button": {
                "text": instance.about_section_primary_button_text,
                "url": instance.about_section_primary_button_url,
            },
            "secondary_button": {
                "text": instance.about_section_secondary_button_text,
                "url": instance.about_section_secondary_button_url,
            },
        }


class NetworkSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "title": instance.network_section_title,
            "video_url": _absolute_url(instance.network_section_video, request),
            "stats": instance.network_stats(),
        }


class TalentPoolSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "title": instance.talent_pool_section_title,
            "subtitle": instance.talent_pool_section_subtitle,
            "description": instance.talent_pool_section_description,
            "image": _absolute_url(instance.talent_pool_section_image, request),
            "primary_button": {
                "text": instance.talent_pool_section_primary_button_text,
                "url": instance.talent_pool_section_primary_button_url,
            },
            "secondary_button": {
                "text": instance.talent_pool_section_secondary_button_text,
                "url": instance.talent_pool_section_secondary_button_url,
            },
        }


class ApplyCompanySerializer(serializers.Serializer):
    """Single apply-section company card — from `ApplySection.apply_companies()`."""

    position = serializers.IntegerField()
    label = serializers.CharField(allow_blank=True)
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    button_text = serializers.CharField(allow_blank=True)
    button_url = serializers.URLField(allow_blank=True)
    large_image = serializers.SerializerMethodField()
    small_image = serializers.SerializerMethodField()

    def get_large_image(self, obj):
        return _absolute_url(obj.get("large_image"), self.context.get("request"))

    def get_small_image(self, obj):
        return _absolute_url(obj.get("small_image"), self.context.get("request"))


class ApplySectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "title": instance.apply_section_title,
            "subtitle": instance.apply_section_subtitle,
            "companies": ApplyCompanySerializer(
                instance.apply_companies(),
                many=True,
                context=self.context,
            ).data,
            "bottom_button": {
                "text": instance.apply_section_bottom_button_text,
                "url": instance.apply_section_bottom_button_url,
            },
        }


class HomePageSerializer(serializers.Serializer):
    """Combined homepage payload — every section in one response for Next.js."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "hero": HeroSectionSerializer(HeroSection.load(), context=ctx).data,
            "features": FeatureSectionSerializer(FeatureSection.load(), context=ctx).data,
            "about": AboutSectionSerializer(AboutSection.load(), context=ctx).data,
            "network": NetworkSectionSerializer(NetworkSection.load(), context=ctx).data,
            "talent_pool": TalentPoolSectionSerializer(TalentPoolSection.load(), context=ctx).data,
            "apply": ApplySectionSerializer(ApplySection.load(), context=ctx).data,
        }
