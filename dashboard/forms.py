"""Dashboard ModelForms."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from home.models import (
    APP_BUTTON_COUNT,
    TESTIMONIAL_USER_COUNT,
    AboutSection,
    AppSection,
    ApplyCompany,
    ApplySection,
    FeatureCard,
    FeatureSection,
    FooterLink,
    FooterSettings,
    HeaderSettings,
    HeaderTab,
    HeroSection,
    NetworkSection,
    NetworkStat,
    SocialMediaCard,
    SocialMediaSection,
    TalentPoolSection,
    TestimonialsSection,
)


class CleanFileInput(forms.ClearableFileInput):
    """File input that still processes the `{name}-clear` POST flag (so the
    custom dashboard preview's cross icon can mark a stored image for
    deletion) but renders only a plain file input — no default
    'Currently / Change / Clear' chrome."""

    template_name = "django/forms/widgets/file.html"


class BootstrapFormMixin:
    """Add `form-control` (or appropriate) classes to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault("class", "form-control")
            elif isinstance(widget, forms.FileInput):
                widget.attrs.setdefault("class", "form-control-file")
            else:
                widget.attrs.setdefault("class", "form-control")


class DashboardLoginForm(BootstrapFormMixin, AuthenticationForm):
    pass


class FooterSettingsForm(BootstrapFormMixin, forms.ModelForm):
    """Site-wide footer — logo and contact / legal copy. Links are managed
    via the inline `FooterLinkFormSet`."""

    class Meta:
        model = FooterSettings
        fields = ["logo", "title", "address", "email", "copyright_text"]
        widgets = {
            "logo": CleanFileInput(),
            "address": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "logo": "Footer Logo",
            "title": "Title",
            "address": "Address",
            "email": "Email",
            "copyright_text": "Copyright Text",
        }


class FooterLinkForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FooterLink
        fields = ["label", "url"]
        labels = {"label": "Label", "url": "URL"}


FooterLinkFormSet = forms.inlineformset_factory(
    FooterSettings,
    FooterLink,
    form=FooterLinkForm,
    extra=0,
    can_delete=True,
)


class HeaderSettingsForm(BootstrapFormMixin, forms.ModelForm):
    """Site-wide header — logo and CTA button. Tabs live on the inline
    `HeaderTabFormSet`."""

    class Meta:
        model = HeaderSettings
        fields = ["logo", "button_text", "button_url"]
        widgets = {"logo": CleanFileInput()}
        labels = {
            "logo": "Header Logo",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class HeaderTabForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = HeaderTab
        fields = ["label", "url"]
        labels = {"label": "Tab Name", "url": "Tab Link"}


HeaderTabFormSet = forms.inlineformset_factory(
    HeaderSettings,
    HeaderTab,
    form=HeaderTabForm,
    extra=0,
    can_delete=True,
)


class HeroSectionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = [
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
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "background_image": CleanFileInput(),
            "hero_image": CleanFileInput(),
        }
        labels = {
            "title": "Title",
            "description": "Description",
        }


class FeatureSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Feature section editor — section heading + shared card button text.
    Cards live on the inline `FeatureCardFormSet`."""

    class Meta:
        model = FeatureSection
        fields = [
            "features_title",
            "features_description",
            "features_button_text",
        ]
        widgets = {
            "features_description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "features_title": "Title",
            "features_description": "Description",
            "features_button_text": "Button Text (shared across all cards)",
        }


class FeatureCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FeatureCard
        fields = ["title", "icon", "button_url"]
        widgets = {"icon": CleanFileInput()}
        labels = {"title": "Title", "icon": "Icon", "button_url": "Button URL"}


FeatureCardFormSet = forms.inlineformset_factory(
    FeatureSection,
    FeatureCard,
    form=FeatureCardForm,
    extra=0,
    can_delete=True,
)


class NetworkSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Stats / Network section editor — section heading + optional video
    upload. Stats live on the inline `NetworkStatFormSet`."""

    class Meta:
        model = NetworkSection
        fields = [
            "network_section_title",
            "network_section_video",
        ]
        widgets = {
            "network_section_video": CleanFileInput(attrs={"accept": "video/*"}),
        }
        labels = {
            "network_section_title": "Title",
            "network_section_video": "Video",
        }


class NetworkStatForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = NetworkStat
        fields = ["value", "label"]
        labels = {"value": "Value", "label": "Label"}


NetworkStatFormSet = forms.inlineformset_factory(
    NetworkSection,
    NetworkStat,
    form=NetworkStatForm,
    extra=0,
    can_delete=True,
)


class ApplySectionForm(BootstrapFormMixin, forms.ModelForm):
    """Apply section editor — heading + sub-heading + bottom button. Company
    cards live on the inline `ApplyCompanyFormSet`."""

    class Meta:
        model = ApplySection
        fields = [
            "apply_section_title",
            "apply_section_subtitle",
            "apply_section_bottom_button_text",
            "apply_section_bottom_button_url",
        ]
        labels = {
            "apply_section_title": "Title",
            "apply_section_subtitle": "Sub-title",
            "apply_section_bottom_button_text": "Bottom Button Text",
            "apply_section_bottom_button_url": "Bottom Button URL",
        }


class ApplyCompanyForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ApplyCompany
        fields = [
            "label",
            "title",
            "description",
            "button_text",
            "button_url",
            "large_image",
            "small_image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "large_image": CleanFileInput(),
            "small_image": CleanFileInput(),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
            "large_image": "Large Image",
            "small_image": "Small Image",
        }


ApplyCompanyFormSet = forms.inlineformset_factory(
    ApplySection,
    ApplyCompany,
    form=ApplyCompanyForm,
    extra=0,
    can_delete=True,
)


class TalentPoolSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Talent Pool section editor — same shape as About + a subtitle."""

    class Meta:
        model = TalentPoolSection
        fields = [
            "talent_pool_section_title",
            "talent_pool_section_subtitle",
            "talent_pool_section_description",
            "talent_pool_section_primary_button_text",
            "talent_pool_section_primary_button_url",
            "talent_pool_section_secondary_button_text",
            "talent_pool_section_secondary_button_url",
            "talent_pool_section_image",
        ]
        widgets = {
            "talent_pool_section_description": forms.Textarea(attrs={"rows": 5}),
            "talent_pool_section_image": CleanFileInput(),
        }
        labels = {
            "talent_pool_section_title": "Title",
            "talent_pool_section_subtitle": "Subtitle",
            "talent_pool_section_description": "Description",
            "talent_pool_section_primary_button_text": "Primary Button Text",
            "talent_pool_section_primary_button_url": "Primary Button URL",
            "talent_pool_section_secondary_button_text": "Secondary Button Text",
            "talent_pool_section_secondary_button_url": "Secondary Button URL",
            "talent_pool_section_image": "Side Image",
        }


class SocialMediaSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Social Media section — just the heading. Cards live on the inline formset."""

    class Meta:
        model = SocialMediaSection
        fields = ["heading"]
        labels = {"heading": "Title"}


class SocialMediaCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SocialMediaCard
        fields = ["name", "icon"]
        widgets = {"icon": CleanFileInput()}
        labels = {"name": "Name", "icon": "Icon"}


SocialMediaCardFormSet = forms.inlineformset_factory(
    SocialMediaSection,
    SocialMediaCard,
    form=SocialMediaCardForm,
    extra=0,
    can_delete=True,
)


def _testimonial_user_field_names() -> list[str]:
    """Flat list of the 9 per-user fields, in user-then-field order."""
    suffixes = ("name", "profile_image", "message")
    return [
        f"testimonial_{i}_{suffix}"
        for i in range(1, TESTIMONIAL_USER_COUNT + 1)
        for suffix in suffixes
    ]


class TestimonialsSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Testimonials section editor — background image + 3 fixed users."""

    class Meta:
        model = TestimonialsSection
        fields = [
            "title",
            "background_image",
            *_testimonial_user_field_names(),
        ]
        widgets = {
            "background_image": CleanFileInput(),
            **{
                f"testimonial_{i}_profile_image": CleanFileInput()
                for i in range(1, TESTIMONIAL_USER_COUNT + 1)
            },
            **{
                f"testimonial_{i}_message": forms.Textarea(attrs={"rows": 3})
                for i in range(1, TESTIMONIAL_USER_COUNT + 1)
            },
        }
        labels = {
            "title": "Title",
            "background_image": "Background Image",
            **{f"testimonial_{i}_name": "Name" for i in range(1, TESTIMONIAL_USER_COUNT + 1)},
            **{f"testimonial_{i}_profile_image": "Profile Image" for i in range(1, TESTIMONIAL_USER_COUNT + 1)},
            **{f"testimonial_{i}_message": "Message" for i in range(1, TESTIMONIAL_USER_COUNT + 1)},
        }

    def user_groups(self):
        """Yield `(position, fields_dict)` tuples so the template can loop users."""
        for i in range(1, TESTIMONIAL_USER_COUNT + 1):
            yield i, {
                "name": self[f"testimonial_{i}_name"],
                "profile_image": self[f"testimonial_{i}_profile_image"],
                "message": self[f"testimonial_{i}_message"],
            }


def _app_button_field_names() -> list[str]:
    return [
        f"button_{i}_{suffix}"
        for i in range(1, APP_BUTTON_COUNT + 1)
        for suffix in ("text", "url")
    ]


class AppSectionForm(BootstrapFormMixin, forms.ModelForm):
    """App section editor — title, description, 3 buttons, side image, barcode."""

    class Meta:
        model = AppSection
        fields = [
            "title",
            "description",
            *_app_button_field_names(),
            "side_image",
            "barcode_image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "side_image": CleanFileInput(),
            "barcode_image": CleanFileInput(),
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "side_image": "Side Image",
            "barcode_image": "Barcode Image",
            **{f"button_{i}_text": "Text" for i in range(1, APP_BUTTON_COUNT + 1)},
            **{f"button_{i}_url": "URL" for i in range(1, APP_BUTTON_COUNT + 1)},
        }

    def button_groups(self):
        for i in range(1, APP_BUTTON_COUNT + 1):
            yield i, {
                "text": self[f"button_{i}_text"],
                "url": self[f"button_{i}_url"],
            }


class AboutSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About / Mission section editor."""

    class Meta:
        model = AboutSection
        fields = [
            "about_section_label",
            "about_section_title",
            "about_section_description",
            "about_section_primary_button_text",
            "about_section_primary_button_url",
            "about_section_secondary_button_text",
            "about_section_secondary_button_url",
            "about_section_image",
        ]
        widgets = {
            "about_section_description": forms.Textarea(attrs={"rows": 5}),
            "about_section_image": CleanFileInput(),
        }
        labels = {
            "about_section_label": "Label",
            "about_section_title": "Title",
            "about_section_description": "Description",
            "about_section_primary_button_text": "Primary Button Text",
            "about_section_primary_button_url": "Primary Button URL",
            "about_section_secondary_button_text": "Secondary Button Text",
            "about_section_secondary_button_url": "Secondary Button URL",
            "about_section_image": "Side Image",
        }
