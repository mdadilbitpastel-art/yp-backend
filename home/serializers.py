"""DRF serializers for the home app."""

from rest_framework import serializers

from data_management.models import section_images

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


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


def _images_payload(section, request):
    return [_absolute_url(row["image"], request) for row in section_images(section)]


class HeaderTabSerializer(serializers.Serializer):
    label = serializers.CharField()
    url = serializers.CharField(allow_blank=True)


class HeaderSettingsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "logo": _absolute_url(instance.logo, request),
            "button_text": instance.button_text,
            "button_url": instance.button_url,
            "tabs": HeaderTabSerializer(
                instance.tabs.all().order_by("order", "id"),
                many=True,
                context=self.context,
            ).data,
        }


class FooterLinkSerializer(serializers.Serializer):
    label = serializers.CharField()
    url = serializers.URLField(allow_blank=True)


class FooterSettingsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "logo": _absolute_url(instance.logo, request),
            "title": instance.title,
            "address": instance.address,
            "email": instance.email,
            "copyright_text": instance.copyright_text,
            "links": FooterLinkSerializer(
                instance.links.all().order_by("order", "id"),
                many=True,
                context=self.context,
            ).data,
        }


class HeroSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        rating = instance.rating
        return {
            "id": instance.pk,
            "title": instance.title,
            "description": instance.description,
            "highlight_text": instance.highlight_text,
            "primary_button": {
                "text": instance.primary_button_text,
                "url": instance.primary_button_url,
            },
            "secondary_button": {
                "text": instance.secondary_button_text,
                "url": instance.secondary_button_url,
            },
            "rating": float(rating) if rating is not None else None,
            "bottom_note": instance.bottom_note,
            "images": _images_payload(instance, request),
        }


class FeatureCardSerializer(serializers.Serializer):
    """Single feature card — built from `FeatureSection.feature_cards()` dicts."""

    position = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    icon = serializers.SerializerMethodField()
    button_url = serializers.URLField(allow_blank=True)

    def get_icon(self, obj):
        return _absolute_url(obj.get("icon"), self.context.get("request"))


class FeatureSectionSerializer(serializers.Serializer):
    """Feature section — title/description plus the active cards as a list."""

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
            "images": _images_payload(instance, request),
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
            "label": instance.talent_pool_section_label,
            "title": instance.talent_pool_section_title,
            "subtitle": instance.talent_pool_section_subtitle,
            "description": instance.talent_pool_section_description,
            "images": _images_payload(instance, request),
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
    image = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _absolute_url(obj.get("large_image"), self.context.get("request"))

    def get_logo(self, obj):
        return _absolute_url(obj.get("small_image"), self.context.get("request"))


class ApplyEmployerSerializer(serializers.Serializer):
    """Logo picker entry pulled from Data Management → Employers."""

    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    logo = serializers.SerializerMethodField()
    description = serializers.CharField(allow_blank=True)
    url = serializers.URLField(allow_blank=True)

    def get_logo(self, obj):
        return _absolute_url(obj.get("logo"), self.context.get("request"))


def _employer_picker_payload(section, context):
    return ApplyEmployerSerializer(
        [
            {
                "position": index,
                "name": e.name,
                "logo": e.logo if e.logo else None,
                "description": e.description,
                "url": e.url,
            }
            for index, e in enumerate(section.selected_employers.all(), start=1)
        ],
        many=True,
        context=context,
    ).data


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
            "employer_logos": _employer_picker_payload(instance, self.context),
            "bottom_button": {
                "text": instance.apply_section_bottom_button_text,
                "url": instance.apply_section_bottom_button_url,
            },
        }


class SocialMediaCardSerializer(serializers.Serializer):
    """Single social-media card — built from `SocialMediaSection.social_cards()`."""

    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        return _absolute_url(obj.get("icon"), self.context.get("request"))


class SocialMediaSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "heading": instance.heading,
            "subtitle": instance.subtitle,
            "cards": SocialMediaCardSerializer(
                instance.social_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class TestimonialUserSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    profile_image = serializers.SerializerMethodField()
    message = serializers.CharField(allow_blank=True)

    def get_profile_image(self, obj):
        return _absolute_url(obj.get("profile_image"), self.context.get("request"))


class TestimonialsSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "title": instance.title,
            "images": _images_payload(instance, request),
            "users": TestimonialUserSerializer(
                instance.testimonials(),
                many=True,
                context=self.context,
            ).data,
        }


class AppButtonSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    text = serializers.CharField(allow_blank=True)
    url = serializers.URLField(allow_blank=True)


class AppSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "title": instance.title,
            "description": instance.description,
            "buttons": AppButtonSerializer(
                instance.buttons(),
                many=True,
                context=self.context,
            ).data,
            "bottom_note": instance.bottom_note,
            "images": _images_payload(instance, request),
        }


class HomePageSerializer(serializers.Serializer):
    """Combined homepage payload — every section in one response for Next.js."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "header": HeaderSettingsSerializer(HeaderSettings.load(), context=ctx).data,
            "hero": HeroSectionSerializer(HeroSection.load(), context=ctx).data,
            "features": FeatureSectionSerializer(FeatureSection.load(), context=ctx).data,
            "about": AboutSectionSerializer(AboutSection.load(), context=ctx).data,
            "network": NetworkSectionSerializer(NetworkSection.load(), context=ctx).data,
            "talent_pool": TalentPoolSectionSerializer(TalentPoolSection.load(), context=ctx).data,
            "apply": ApplySectionSerializer(ApplySection.load(), context=ctx).data,
            "social_media": SocialMediaSectionSerializer(SocialMediaSection.load(), context=ctx).data,
            "testimonials": TestimonialsSectionSerializer(TestimonialsSection.load(), context=ctx).data,
            "app": AppSectionSerializer(AppSection.load(), context=ctx).data,
            "footer": FooterSettingsSerializer(FooterSettings.load(), context=ctx).data,
        }
