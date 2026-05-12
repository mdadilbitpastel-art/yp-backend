"""DRF serializers for the insight app."""

from rest_framework import serializers

from data_management.models import section_images

from .models import (
    InsightArticleSection,
    InsightFounderSection,
    InsightHeroSection,
    InsightLaneSection,
    InsightSubscribeSection,
)


def _absolute_url(image, request):
    if not image:
        return None
    return request.build_absolute_uri(image.url) if request else image.url


def _images_payload(section, request):
    return [_absolute_url(row["image"], request) for row in section_images(section)]


class InsightHeroSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "search_placeholder": instance.search_placeholder,
        }


class InsightFounderCategorySerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)


class InsightFounderSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label_1": instance.label_1,
            "label_2": instance.label_2,
            "date_label": instance.date_label,
            "title": instance.title,
            "description": instance.description,
            "meta_data": instance.meta_data,
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
            "categories": InsightFounderCategorySerializer(
                instance.categories(),
                many=True,
                context=self.context,
            ).data,
            "images": _images_payload(instance, request),
        }


class InsightArticleCardSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    label = serializers.CharField(allow_blank=True)
    image = serializers.SerializerMethodField()
    date_label = serializers.CharField(allow_blank=True)
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    tag = serializers.CharField(allow_blank=True)
    button_url = serializers.URLField(allow_blank=True)

    def get_image(self, obj):
        return _absolute_url(obj.get("image"), self.context.get("request"))


class InsightArticleSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "title": instance.title,
            "card_button_text": instance.card_button_text,
            "cards": InsightArticleCardSerializer(
                instance.cards(),
                many=True,
                context=self.context,
            ).data,
        }


class InsightLaneSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True)
    article_count = serializers.IntegerField()
    url = serializers.URLField(allow_blank=True)


class InsightLaneSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "label": instance.label,
            "title": instance.title,
            "lanes": InsightLaneSerializer(
                instance.lanes(),
                many=True,
                context=self.context,
            ).data,
        }


class InsightSubscribeSectionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        request = self.context.get("request")
        return {
            "label": instance.label,
            "title": instance.title,
            "description": instance.description,
            "email_placeholder": instance.email_placeholder,
            "button": {
                "text": instance.button_text,
                "url": instance.button_url,
            },
            "bottom_note": instance.bottom_note,
            "images": _images_payload(instance, request),
        }


class InsightPageSerializer(serializers.Serializer):
    """Combined Insight page payload — every section in one response."""

    def to_representation(self, _instance):
        ctx = self.context
        return {
            "hero": InsightHeroSectionSerializer(InsightHeroSection.load(), context=ctx).data,
            "founder": InsightFounderSectionSerializer(InsightFounderSection.load(), context=ctx).data,
            "article": InsightArticleSectionSerializer(InsightArticleSection.load(), context=ctx).data,
            "lane": InsightLaneSectionSerializer(InsightLaneSection.load(), context=ctx).data,
            "subscribe": InsightSubscribeSectionSerializer(InsightSubscribeSection.load(), context=ctx).data,
        }
