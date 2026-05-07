"""DRF serializers for the about_us app."""

from rest_framework import serializers

from .models import (
    AboutUsCommunitySection,
    AboutUsFounderSection,
    AboutUsHeroSection,
    AboutUsJourneySection,
    AboutUsMissionSection,
    AboutUsPledgeSection,
    AboutUsTeamSection,
    AboutUsValuesSection,
)


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


class AboutUsHeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsHeroSection
        fields = [
            "id",
            "label",
            "title",
            "description",
            "background_image",
        ]


class AboutUsMissionSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "side_image": _absolute_url(instance.side_image, request),
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
    email_icon = serializers.SerializerMethodField()
    email_url = serializers.CharField(allow_blank=True)
    view_profile_text = serializers.CharField(allow_blank=True)
    view_profile_url = serializers.URLField(allow_blank=True)

    def get_profile_image(self, obj):
        return _absolute_url(obj.get("profile_image"), self.context.get("request"))

    def get_email_icon(self, obj):
        return _absolute_url(obj.get("email_icon"), self.context.get("request"))


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
            "side_image": _absolute_url(instance.side_image, request),
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
            "side_image": _absolute_url(instance.side_image, request),
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
        }
