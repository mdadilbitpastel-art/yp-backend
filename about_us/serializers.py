"""DRF serializers for the about_us app."""

from rest_framework import serializers

from data_management.models import section_images

from about_us.models import (
    AboutUsCommunitySection,
    AboutUsFounderSection,
    AboutUsHeroSection,
    AboutUsJourneySection,
    AboutUsMissionSection,
    AboutUsPledgeSection,
    AboutUsSocialMediaSection,
    AboutUsTeamSection,
    AboutUsValuesSection,
)


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


def _images_payload(section, request):
    return [_absolute_url(row["image"], request) for row in section_images(section)]


class AboutUsHeroSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "id": instance.pk,
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "images": _images_payload(instance, request),
        }


class AboutUsMissionSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "images": _images_payload(instance, request),
            "stats": instance.mission_stats(),
        }


class AboutUsValueCardSerializer(serializers.Serializer):
    """Single value card — built from `AboutUsValuesSection.value_cards()` dicts."""

    position = serializers.IntegerField()
    icon = serializers.SerializerMethodField()
    label = serializers.CharField(allow_blank=True)
    note = serializers.CharField(allow_blank=True)

    def get_icon(self, obj):
        return _absolute_url(obj.get("icon"), self.context.get("request"))


class AboutUsValuesSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "subtitle": instance.subtitle,
            "cards": AboutUsValueCardSerializer(
                instance.value_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class AboutUsCommunityCardSerializer(serializers.Serializer):
    """Single community card — built from `AboutUsCommunitySection.community_cards()` dicts."""

    position = serializers.IntegerField()
    image = serializers.SerializerMethodField()
    name = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    button = serializers.SerializerMethodField()

    def get_image(self, obj):
        return _absolute_url(obj.get("image"), self.context.get("request"))

    def get_button(self, obj):
        return {
            "text": obj.get("button_text", ""),
            "url": obj.get("button_url", ""),
        }


class AboutUsCommunitySectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "subtitle": instance.subtitle,
            "cards": AboutUsCommunityCardSerializer(
                instance.community_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class AboutUsTeamMemberSerializer(serializers.Serializer):
    """Single team member card — built from `AboutUsTeamSection.team_members()` dicts."""

    position = serializers.IntegerField()
    profile_image = serializers.SerializerMethodField()
    name = serializers.CharField(allow_blank=True)
    designation = serializers.CharField(allow_blank=True)
    email_url = serializers.CharField(allow_blank=True)
    view_profile_text = serializers.CharField(allow_blank=True)
    view_profile_url = serializers.URLField(allow_blank=True)

    def get_profile_image(self, obj):
        return _absolute_url(obj.get("profile_image"), self.context.get("request"))


class AboutUsTeamSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "subtitle": instance.subtitle,
            "members": AboutUsTeamMemberSerializer(
                instance.team_members(),
                many=True,
                context=self.context,
            ).data,
        }


class AboutUsPledgeSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "images": _images_payload(instance, request),
        }


class AboutUsJourneyCardSerializer(serializers.Serializer):
    """Single journey card — built from `AboutUsJourneySection.journey_cards()` dicts."""

    position = serializers.IntegerField()
    image = serializers.SerializerMethodField()
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)

    def get_image(self, obj):
        return _absolute_url(obj.get("image"), self.context.get("request"))


class AboutUsJourneySectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "subtitle": instance.subtitle,
            "cards": AboutUsJourneyCardSerializer(
                instance.journey_cards(),
                many=True,
                context=self.context,
            ).data,
        }


class AboutUsFounderSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.label,
            "founder_name": instance.founder_name,
            "designation": instance.designation,
            "description": instance.description,
            "founder_message": instance.founder_message,
            "images": _images_payload(instance, request),
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
        }


class AboutUsSocialMediaCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        return _absolute_url(obj.get("icon"), self.context.get("request"))


class AboutUsSocialMediaSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        cards = [
            {
                "position": index,
                "name": entry.name,
                "icon": entry.icon if entry.icon else None,
            }
            for index, entry in enumerate(instance.selected_social_media.all(), start=1)
        ]
        return {
            "label": instance.label,
            "heading": instance.heading,
            "subtitle": instance.subtitle,
            "cards": AboutUsSocialMediaCardSerializer(
                cards, many=True, context=self.context
            ).data,
        }


class AboutUsPageSerializer(serializers.Serializer):
    """Combined About Us page payload — every section in one response."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "hero": AboutUsHeroSectionSerializer(AboutUsHeroSection.load(), context=ctx).data,
            "mission": AboutUsMissionSectionSerializer(AboutUsMissionSection.load(), context=ctx).data,
            "founder": AboutUsFounderSectionSerializer(AboutUsFounderSection.load(), context=ctx).data,
            "values": AboutUsValuesSectionSerializer(AboutUsValuesSection.load(), context=ctx).data,
            "journey": AboutUsJourneySectionSerializer(AboutUsJourneySection.load(), context=ctx).data,
            "pledge": AboutUsPledgeSectionSerializer(AboutUsPledgeSection.load(), context=ctx).data,
            "team": AboutUsTeamSectionSerializer(AboutUsTeamSection.load(), context=ctx).data,
            "community": AboutUsCommunitySectionSerializer(AboutUsCommunitySection.load(), context=ctx).data,
            "social_media": AboutUsSocialMediaSectionSerializer(AboutUsSocialMediaSection.load(), context=ctx).data,
        }
