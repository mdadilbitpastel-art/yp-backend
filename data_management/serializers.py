"""DRF serializers for the shared Data Management models."""

from rest_framework import serializers

from .models import Employer, SocialMediaIcon, Statistic, TeamMember


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ["id", "value", "label", "order"]


class EmployerSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Employer
        fields = ["id", "name", "logo", "description", "url", "order"]

    def get_logo(self, obj):
        return _absolute_url(obj.logo, self.context.get("request"))


class TeamMemberSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "profile_image",
            "designation",
            "email_url",
            "view_profile_text",
            "view_profile_url",
            "order",
        ]

    def get_profile_image(self, obj):
        return _absolute_url(obj.profile_image, self.context.get("request"))


class SocialMediaIconSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = SocialMediaIcon
        fields = ["id", "name", "icon", "order"]

    def get_icon(self, obj):
        return _absolute_url(obj.icon, self.context.get("request"))
