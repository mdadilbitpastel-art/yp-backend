"""Dashboard ModelForms."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from home.models import (
    APP_BUTTON_COUNT,
    APPLY_COMPANY_COUNT,
    FEATURE_CARD_COUNT,
    NETWORK_STAT_COUNT,
    TESTIMONIAL_USER_COUNT,
    AboutSection,
    AppSection,
    ApplySection,
    FeatureSection,
    FooterLink,
    FooterSettings,
    HeaderSettings,
    HeroSection,
    NetworkSection,
    SocialMediaCard,
    SocialMediaSection,
    TalentPoolSection,
    TestimonialsSection,
)


class CleanFileInput(forms.FileInput):
    """Plain file input — no 'Currently / Change / Clear' chrome."""


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


def _default_tab_label(module_title: str) -> str:
    """Strip the trailing ' Management' suffix used in module titles."""
    suffix = " Management"
    if module_title.endswith(suffix):
        return module_title[: -len(suffix)]
    return module_title


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
    """Site-wide header — logo, CTA button, plus a dynamic editable label
    per registered (non-header) management module."""

    TAB_FIELD_PREFIX = "tab_label__"

    class Meta:
        model = HeaderSettings
        fields = ["logo", "button_text", "button_url"]
        widgets = {"logo": CleanFileInput()}
        labels = {
            "logo": "Header Logo",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Local import to avoid a circular reference with the sections registry.
        from .sections import DASHBOARD_MODULES

        stored = (self.instance.tab_labels or {}) if self.instance else {}
        self._tab_modules = []
        for module in DASHBOARD_MODULES:
            # Skip flat modules (Header itself, Footer, …) — header tabs only
            # represent content management modules, not site-chrome modules.
            if module.get("flat"):
                continue
            key = module["key"]
            field_name = f"{self.TAB_FIELD_PREFIX}{key}"
            self.fields[field_name] = forms.CharField(
                required=False,
                max_length=80,
                label=_default_tab_label(module["title"]),
                initial=stored.get(key) or _default_tab_label(module["title"]),
            )
            self.fields[field_name].widget.attrs.setdefault("class", "form-control")
            self._tab_modules.append((module, field_name))

    def tab_fields(self):
        """Yield `(module, bound_field)` so the template can render the
        editable list of header tab labels."""
        for module, field_name in self._tab_modules:
            yield module, self[field_name]

    def save(self, commit=True):
        instance = super().save(commit=False)
        labels = {}
        for module, field_name in self._tab_modules:
            value = (self.cleaned_data.get(field_name) or "").strip()
            if value:
                labels[module["key"]] = value
        instance.tab_labels = labels
        if commit:
            instance.save()
        return instance


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


def _feature_card_field_names() -> list[str]:
    """Flat list of the 15 per-card fields, in card-then-field order."""
    suffixes = (
        "title",
        "icon",
        "button_url",
    )
    return [
        f"feature_{i}_{suffix}"
        for i in range(1, FEATURE_CARD_COUNT + 1)
        for suffix in suffixes
    ]


class FeatureSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Feature section editor — section heading + 5 fixed cards."""

    class Meta:
        model = FeatureSection
        fields = [
            "features_title",
            "features_description",
            "features_button_text",
            *_feature_card_field_names(),
        ]
        widgets = {
            "features_description": forms.Textarea(attrs={"rows": 3}),
            **{f"feature_{i}_icon": CleanFileInput() for i in range(1, FEATURE_CARD_COUNT + 1)},
        }
        labels = {
            "features_title": "Title",
            "features_description": "Description",
            "features_button_text": "Button Text (shared across all cards)",
            **{f"feature_{i}_title": "Title" for i in range(1, FEATURE_CARD_COUNT + 1)},
            **{f"feature_{i}_icon": "Icon" for i in range(1, FEATURE_CARD_COUNT + 1)},
            **{f"feature_{i}_button_url": "Button URL" for i in range(1, FEATURE_CARD_COUNT + 1)},
        }

    def card_groups(self):
        """Yield `(position, fields_dict)` tuples so the template can loop cards."""
        for i in range(1, FEATURE_CARD_COUNT + 1):
            yield i, {
                "title": self[f"feature_{i}_title"],
                "icon": self[f"feature_{i}_icon"],
                "button_url": self[f"feature_{i}_button_url"],
            }


def _network_stat_field_names() -> list[str]:
    """Flat list of the 8 per-stat fields, in stat-then-field order."""
    suffixes = ("value", "label")
    return [
        f"network_stat_{i}_{suffix}"
        for i in range(1, NETWORK_STAT_COUNT + 1)
        for suffix in suffixes
    ]


class NetworkSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Stats / Network section editor — section heading + 4 fixed stats."""

    class Meta:
        model = NetworkSection
        fields = [
            "network_section_title",
            "network_section_video_url",
            *_network_stat_field_names(),
        ]
        labels = {
            "network_section_title": "Title",
            "network_section_video_url": "Video URL",
            **{f"network_stat_{i}_value": "Value" for i in range(1, NETWORK_STAT_COUNT + 1)},
            **{f"network_stat_{i}_label": "Label" for i in range(1, NETWORK_STAT_COUNT + 1)},
        }

    def stat_groups(self):
        """Yield `(position, fields_dict)` tuples so the template can loop stats."""
        for i in range(1, NETWORK_STAT_COUNT + 1):
            yield i, {
                "value": self[f"network_stat_{i}_value"],
                "label": self[f"network_stat_{i}_label"],
            }


def _apply_company_field_names() -> list[str]:
    """Flat list of the 21 per-company fields, in company-then-field order."""
    suffixes = (
        "label",
        "title",
        "description",
        "button_text",
        "button_url",
        "large_image",
        "small_image",
    )
    return [
        f"apply_company_{i}_{suffix}"
        for i in range(1, APPLY_COMPANY_COUNT + 1)
        for suffix in suffixes
    ]


class ApplySectionForm(BootstrapFormMixin, forms.ModelForm):
    """Apply section editor — heading + sub-heading + 3 fixed company cards."""

    class Meta:
        model = ApplySection
        fields = [
            "apply_section_title",
            "apply_section_subtitle",
            *_apply_company_field_names(),
            "apply_section_bottom_button_text",
            "apply_section_bottom_button_url",
        ]
        widgets = {
            **{
                f"apply_company_{i}_description": forms.Textarea(attrs={"rows": 3})
                for i in range(1, APPLY_COMPANY_COUNT + 1)
            },
            **{
                f"apply_company_{i}_large_image": CleanFileInput()
                for i in range(1, APPLY_COMPANY_COUNT + 1)
            },
            **{
                f"apply_company_{i}_small_image": CleanFileInput()
                for i in range(1, APPLY_COMPANY_COUNT + 1)
            },
        }
        labels = {
            "apply_section_title": "Heading",
            "apply_section_subtitle": "Sub-heading",
            "apply_section_bottom_button_text": "Bottom Button Text",
            "apply_section_bottom_button_url": "Bottom Button URL",
            **{f"apply_company_{i}_label": "Label" for i in range(1, APPLY_COMPANY_COUNT + 1)},
            **{f"apply_company_{i}_title": "Title" for i in range(1, APPLY_COMPANY_COUNT + 1)},
            **{f"apply_company_{i}_description": "Description" for i in range(1, APPLY_COMPANY_COUNT + 1)},
            **{f"apply_company_{i}_button_text": "Button Text" for i in range(1, APPLY_COMPANY_COUNT + 1)},
            **{f"apply_company_{i}_button_url": "Button URL" for i in range(1, APPLY_COMPANY_COUNT + 1)},
            **{f"apply_company_{i}_large_image": "Large Image" for i in range(1, APPLY_COMPANY_COUNT + 1)},
            **{f"apply_company_{i}_small_image": "Small Image" for i in range(1, APPLY_COMPANY_COUNT + 1)},
        }

    def company_groups(self):
        """Yield `(position, fields_dict)` tuples so the template can loop companies."""
        for i in range(1, APPLY_COMPANY_COUNT + 1):
            yield i, {
                "label": self[f"apply_company_{i}_label"],
                "title": self[f"apply_company_{i}_title"],
                "description": self[f"apply_company_{i}_description"],
                "button_text": self[f"apply_company_{i}_button_text"],
                "button_url": self[f"apply_company_{i}_button_url"],
                "large_image": self[f"apply_company_{i}_large_image"],
                "small_image": self[f"apply_company_{i}_small_image"],
            }


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
        labels = {"heading": "Heading"}


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
