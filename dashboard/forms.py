"""Dashboard ModelForms."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.forms import generic_inlineformset_factory

from about_us.models import (
    AboutUsCommunityCard,
    AboutUsCommunitySection,
    AboutUsFounderSection,
    AboutUsHeroSection,
    AboutUsJourneyCard,
    AboutUsJourneySection,
    AboutUsMissionSection,
    AboutUsPledgeSection,
    AboutUsSocialMediaSection,
    AboutUsTeamSection,
    AboutUsValueCard,
    AboutUsValuesSection,
)
from employers.models import (
    EmployersEventImage,
    EmployersEventsSection,
    EmployersHeroSection,
    EmployersMissionPoint,
    EmployersMissionSection,
    EmployersOfferCard,
    EmployersOfferSection,
)
from partners.models import (
    PartnersCategory,
    PartnersFamilySection,
    PartnersFounderSection,
    PartnersHeroSection,
    PartnersPartnerSection,
    PartnersReviewCard,
    PartnersReviewSection,
)
from events.models import (
    EventsFeaturedSection,
    EventsHeroSection,
    EventsMissedCard,
    EventsMissedSection,
    EventsSubmitSection,
    EventsUpcomingCard,
    EventsUpcomingCategory,
    EventsUpcomingSection,
)
from insight.models import (
    InsightArticleCard,
    InsightArticleSection,
    InsightFounderCategory,
    InsightFounderSection,
    InsightHeroSection,
    InsightLane,
    InsightLaneSection,
    InsightSubscribeSection,
)
from data_management.models import (
    Employer,
    SectionImage,
    SocialMediaIcon,
    Statistic,
    TeamMember,
)
from schools.models import (
    SchoolsBenchmarkCard,
    SchoolsBenchmarkSection,
    SchoolsEmployerSection,
    SchoolsFaqItem,
    SchoolsFaqSection,
    SchoolsHelpCard,
    SchoolsHelpSection,
    SchoolsHeroSection,
    SchoolsSubscribeField,
    SchoolsSubscribeSection,
)
from home.models import (
    APP_BUTTON_COUNT,
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
    SocialMediaSection,
    TalentPoolSection,
    TestimonialsSection,
    TestimonialUser,
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
            "title": forms.TextInput(attrs={"placeholder": "e.g. Stay connected"}),
            "address": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Street, City, Country",
            }),
            "email": forms.EmailInput(attrs={"placeholder": "info@example.com"}),
            "copyright_text": forms.TextInput(attrs={"placeholder": "© 2026 Your Company"}),
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
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Privacy Policy"}),
            "url": forms.URLInput(attrs={"placeholder": "https://example.com/privacy"}),
        }
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
        widgets = {
            "logo": CleanFileInput(),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Get Started"}),
            "button_url": forms.URLInput(attrs={"placeholder": "https://example.com/signup"}),
        }
        labels = {
            "logo": "Header Logo",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class HeaderTabForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = HeaderTab
        fields = ["label", "url"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. About Us"}),
            "url": forms.TextInput(attrs={"placeholder": "/about-us/ or https://…"}),
        }
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
            "rating",
            "bottom_note",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Main headline shown in the hero"}),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph below the headline",
            }),
            "highlight_text": forms.TextInput(attrs={"placeholder": "Word/phrase to highlight"}),
            "primary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Get Started"}),
            "primary_button_url": forms.TextInput(attrs={"placeholder": "/signup or https://…"}),
            "secondary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
            "secondary_button_url": forms.TextInput(attrs={"placeholder": "/about-us or https://…"}),
            "rating": forms.NumberInput(attrs={
                "step": "0.1", "min": "0", "max": "5",
                "placeholder": "4.8",
            }),
            "bottom_note": forms.TextInput(attrs={"placeholder": "Small note under the buttons"}),
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "rating": "Rating (out of 5)",
            "bottom_note": "Bottom Note",
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
            "features_title": forms.TextInput(attrs={"placeholder": "e.g. What we offer"}),
            "features_description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short paragraph introducing the feature cards",
            }),
            "features_button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
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
        widgets = {
            "icon": CleanFileInput(),
            "title": forms.TextInput(attrs={"placeholder": "Card title"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/page or https://…"}),
        }
        labels = {"title": "Title", "icon": "Icon", "button_url": "Button URL"}


FeatureCardFormSet = forms.inlineformset_factory(
    FeatureSection,
    FeatureCard,
    form=FeatureCardForm,
    extra=0,
    can_delete=True,
)


class StatisticPickerMixin:
    """Mixin for forms that expose a `selected_statistics` M2M field.

    Renders the picker as a Select2-enhanced multi-select dropdown
    listing every `Statistic` row from Data Management. Centralised here
    so Home Network, About Us Mission and Partners Hero forms all share
    the same widget."""

    def _configure_statistics_field(self):
        field = self.fields.get("selected_statistics")
        if not field:
            return
        # Swap the widget first — setting `queryset` afterwards populates
        # the new widget's `.choices`, so order matters.
        field.widget = forms.CheckboxSelectMultiple(
            attrs={"class": "statistic-picker"}
        )
        field.queryset = Statistic.objects.all()
        field.required = False
        field.label = "Statistics"
        field.help_text = (
            "Tick the statistics to show in this section. Add or edit the "
            "available statistics from Data Management → Statistics."
        )


class NetworkSectionForm(StatisticPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """Stats / Network section editor — section heading + optional video
    upload + a picker that selects which `Statistic` rows to display."""

    class Meta:
        model = NetworkSection
        fields = [
            "network_section_title",
            "network_section_video",
            "selected_statistics",
        ]
        widgets = {
            "network_section_video": CleanFileInput(attrs={"accept": "video/*"}),
            "network_section_title": forms.TextInput(attrs={"placeholder": "e.g. Our growing network"}),
        }
        labels = {
            "network_section_title": "Title",
            "network_section_video": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_statistics_field()


class StatisticForm(BootstrapFormMixin, forms.ModelForm):
    """Single `Statistic` row — value + label. Used by the Data Management
    page's modelformset for bulk add/edit/delete."""

    class Meta:
        model = Statistic
        fields = ["value", "label"]
        labels = {"value": "Value", "label": "Label"}
        widgets = {
            "value": forms.TextInput(attrs={"placeholder": "e.g. 1,200+"}),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Students placed"}),
        }


StatisticFormSet = forms.modelformset_factory(
    Statistic,
    form=StatisticForm,
    extra=0,
    can_delete=True,
)


class EmployerPickerMixin:
    """Mixin for forms that expose a `selected_employers` M2M field.

    Renders the picker as a plain checkbox list of every `Employer` row
    from Data Management. Mirrors the Statistic picker pattern."""

    def _configure_employers_field(self):
        field = self.fields.get("selected_employers")
        if not field:
            return
        # Swap the widget first — the queryset setter populates choices on
        # whatever widget is current.
        field.widget = forms.CheckboxSelectMultiple(
            attrs={"class": "employer-picker"}
        )
        field.queryset = Employer.objects.all()
        field.required = False
        field.label = "Employers"
        field.help_text = (
            "Tick the employers to show in this section. Add or edit the "
            "available employers from Data Management → Employers."
        )


class EmployerForm(BootstrapFormMixin, forms.ModelForm):
    """Single `Employer` row — name, logo, description, URL. Used by the
    Data Management page's modelformset for bulk add/edit/delete."""

    class Meta:
        model = Employer
        fields = ["name", "logo", "description", "url"]
        widgets = {
            "logo": CleanFileInput(),
            "name": forms.TextInput(attrs={"placeholder": "Company name"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description of the company",
            }),
            "url": forms.URLInput(attrs={"placeholder": "https://example.com"}),
        }
        labels = {
            "name": "Name",
            "logo": "Logo",
            "description": "Description",
            "url": "URL",
        }


EmployerFormSet = forms.modelformset_factory(
    Employer,
    form=EmployerForm,
    extra=0,
    can_delete=True,
)


class SectionImageForm(BootstrapFormMixin, forms.ModelForm):
    """Single image row in the section "Images" card."""

    class Meta:
        model = SectionImage
        fields = ["image"]
        widgets = {"image": CleanFileInput()}
        labels = {"image": ""}


SectionImageFormSet = generic_inlineformset_factory(
    SectionImage,
    form=SectionImageForm,
    ct_field="content_type",
    fk_field="object_id",
    extra=0,
    can_delete=True,
)


class ApplySectionForm(EmployerPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """Apply section editor — heading + sub-heading + bottom button +
    employer picker from Data Management. Company cards live on the
    inline `ApplyCompanyFormSet`."""

    class Meta:
        model = ApplySection
        fields = [
            "apply_section_title",
            "apply_section_subtitle",
            "apply_section_bottom_button_text",
            "apply_section_bottom_button_url",
            "selected_employers",
        ]
        widgets = {
            "apply_section_title": forms.TextInput(attrs={"placeholder": "e.g. Apply to top companies"}),
            "apply_section_subtitle": forms.TextInput(attrs={"placeholder": "Short tagline under the title"}),
            "apply_section_bottom_button_text": forms.TextInput(attrs={"placeholder": "e.g. View All Companies"}),
            "apply_section_bottom_button_url": forms.TextInput(attrs={"placeholder": "/companies or https://…"}),
        }
        labels = {
            "apply_section_title": "Title",
            "apply_section_subtitle": "Sub-title",
            "apply_section_bottom_button_text": "Button Text",
            "apply_section_bottom_button_url": "Button URL",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_employers_field()


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
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description of the company",
            }),
            "large_image": CleanFileInput(),
            "small_image": CleanFileInput(),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Featured"}),
            "title": forms.TextInput(attrs={"placeholder": "Company name"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Apply Now"}),
            "button_url": forms.TextInput(attrs={"placeholder": "https://example.com/apply"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
            "large_image": "Image",
            "small_image": "Logo",
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
            "talent_pool_section_label",
            "talent_pool_section_title",
            "talent_pool_section_subtitle",
            "talent_pool_section_description",
            "talent_pool_section_primary_button_text",
            "talent_pool_section_primary_button_url",
            "talent_pool_section_secondary_button_text",
            "talent_pool_section_secondary_button_url",
        ]
        widgets = {
            "talent_pool_section_description": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Paragraph describing the talent pool",
            }),
            "talent_pool_section_label": forms.TextInput(attrs={"placeholder": "e.g. Talent Pool"}),
            "talent_pool_section_title": forms.TextInput(attrs={"placeholder": "Main title"}),
            "talent_pool_section_subtitle": forms.TextInput(attrs={"placeholder": "Short tagline"}),
            "talent_pool_section_primary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Join Now"}),
            "talent_pool_section_primary_button_url": forms.TextInput(attrs={"placeholder": "/join or https://…"}),
            "talent_pool_section_secondary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
            "talent_pool_section_secondary_button_url": forms.TextInput(attrs={"placeholder": "/about or https://…"}),
        }
        labels = {
            "talent_pool_section_label": "Label",
            "talent_pool_section_title": "Title",
            "talent_pool_section_subtitle": "Subtitle",
            "talent_pool_section_description": "Description",
            "talent_pool_section_primary_button_text": "Primary Button Text",
            "talent_pool_section_primary_button_url": "Primary Button URL",
            "talent_pool_section_secondary_button_text": "Secondary Button Text",
            "talent_pool_section_secondary_button_url": "Secondary Button URL",
        }


class SocialMediaPickerMixin:
    """Mixin for forms that expose a `selected_social_media` M2M field.

    Renders the picker as a plain checkbox list of every
    `SocialMediaIcon` row from Data Management. Mirrors the Statistic /
    Employer picker pattern."""

    def _configure_social_media_field(self):
        field = self.fields.get("selected_social_media")
        if not field:
            return
        # Swap the widget first — the queryset setter populates choices
        # on whatever widget is current.
        field.widget = forms.CheckboxSelectMultiple(
            attrs={"class": "social-media-picker"}
        )
        field.queryset = SocialMediaIcon.objects.all()
        field.required = False
        field.label = "Social Media Icons"
        field.help_text = (
            "Tick the social media icons to show in this section. Add or "
            "edit the available icons from Data Management → Social Media."
        )


class SocialMediaSectionForm(SocialMediaPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """Social Media homepage section — label, heading/title, sub-title.
    Icons are picked from Data Management → Social Media."""

    class Meta:
        model = SocialMediaSection
        fields = ["label", "heading", "subtitle", "selected_social_media"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Follow us"}),
            "heading": forms.TextInput(attrs={"placeholder": "Main title for the section"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "Short tagline"}),
        }
        labels = {
            "label": "Label",
            "heading": "Title",
            "subtitle": "Sub-title",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_social_media_field()


class SocialMediaIconForm(BootstrapFormMixin, forms.ModelForm):
    """Single `SocialMediaIcon` row — name + icon. Used by the Data
    Management page's modelformset for bulk add/edit/delete."""

    class Meta:
        model = SocialMediaIcon
        fields = ["name", "icon"]
        widgets = {
            "icon": CleanFileInput(),
            "name": forms.TextInput(attrs={"placeholder": "e.g. LinkedIn"}),
        }
        labels = {"name": "Name", "icon": "Icon"}


SocialMediaIconFormSet = forms.modelformset_factory(
    SocialMediaIcon,
    form=SocialMediaIconForm,
    extra=0,
    can_delete=True,
)


class TestimonialsSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Testimonials section editor — title only. Background images live on
    `SectionImage`; users live on the inline `TestimonialUserFormSet`."""

    class Meta:
        model = TestimonialsSection
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. What our community says"}),
        }
        labels = {"title": "Title"}


class TestimonialUserForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TestimonialUser
        fields = ["name", "profile_image", "message"]
        widgets = {
            "profile_image": CleanFileInput(),
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "message": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Their testimonial quote",
            }),
        }
        labels = {
            "name": "Name",
            "profile_image": "Profile Image",
            "message": "Message",
        }


TestimonialUserFormSet = forms.inlineformset_factory(
    TestimonialsSection,
    TestimonialUser,
    form=TestimonialUserForm,
    extra=0,
    can_delete=True,
)


def _app_button_field_names() -> list[str]:
    return [
        f"button_{i}_{suffix}"
        for i in range(1, APP_BUTTON_COUNT + 1)
        for suffix in ("text", "url")
    ]


class AppSectionForm(BootstrapFormMixin, forms.ModelForm):
    """App section editor — title, description, 3 buttons, bottom note.
    Images (side + barcode) live on `SectionImage`."""

    class Meta:
        model = AppSection
        fields = [
            "title",
            "description",
            *_app_button_field_names(),
            "bottom_note",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Get our app"}),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about the app",
            }),
            "bottom_note": forms.TextInput(attrs={"placeholder": "Small note under the buttons"}),
            **{
                f"button_{i}_text": forms.TextInput(attrs={"placeholder": "Button label"})
                for i in range(1, APP_BUTTON_COUNT + 1)
            },
            **{
                f"button_{i}_url": forms.TextInput(attrs={"placeholder": "https://…"})
                for i in range(1, APP_BUTTON_COUNT + 1)
            },
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "bottom_note": "Note",
            **{f"button_{i}_text": "Text" for i in range(1, APP_BUTTON_COUNT + 1)},
            **{f"button_{i}_url": "URL" for i in range(1, APP_BUTTON_COUNT + 1)},
        }

    def button_groups(self):
        for i in range(1, APP_BUTTON_COUNT + 1):
            yield i, {
                "text": self[f"button_{i}_text"],
                "url": self[f"button_{i}_url"],
            }


class AboutUsHeroSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — top hero section editor. Images live on `SectionImage`."""

    class Meta:
        model = AboutUsHeroSection
        fields = ["label", "title", "description"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. About Us"}),
            "title": forms.TextInput(attrs={"placeholder": "Main hero title"}),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph below the title",
            }),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
        }


class AboutUsSocialMediaSectionForm(
    SocialMediaPickerMixin, BootstrapFormMixin, forms.ModelForm
):
    """About Us — social media section. Has its own copy of
    label/heading/sub-title (independent of the home page) and its own
    selection of icons from Data Management → Social Media."""

    class Meta:
        model = AboutUsSocialMediaSection
        fields = ["label", "heading", "subtitle", "selected_social_media"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Follow us"}),
            "heading": forms.TextInput(attrs={"placeholder": "Main title for the section"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "Short tagline"}),
        }
        labels = {
            "label": "Label",
            "heading": "Title",
            "subtitle": "Sub-title",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_social_media_field()


class AboutUsCommunitySectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — community section editor. Cards live on the inline
    `AboutUsCommunityCardFormSet`."""

    class Meta:
        model = AboutUsCommunitySection
        fields = ["label", "title", "subtitle"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Community"}),
            "title": forms.TextInput(attrs={"placeholder": "Main title"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "Short tagline"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "subtitle": "Sub-title",
        }


class AboutUsCommunityCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AboutUsCommunityCard
        fields = ["image", "name", "description", "button_text", "button_url"]
        widgets = {
            "image": CleanFileInput(),
            "name": forms.TextInput(attrs={"placeholder": "Card name"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description",
            }),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/page or https://…"}),
        }
        labels = {
            "image": "Image",
            "name": "Name",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


AboutUsCommunityCardFormSet = forms.inlineformset_factory(
    AboutUsCommunitySection,
    AboutUsCommunityCard,
    form=AboutUsCommunityCardForm,
    extra=0,
    can_delete=True,
)


class TeamMemberPickerMixin:
    """Mixin for forms that expose a `selected_team_members` M2M field.

    Renders the picker as a plain checkbox list showing each
    `TeamMember`'s name only. Mirrors the Statistic / Employer /
    SocialMedia picker pattern."""

    def _configure_team_members_field(self):
        field = self.fields.get("selected_team_members")
        if not field:
            return
        field.widget = forms.CheckboxSelectMultiple(
            attrs={"class": "team-member-picker"}
        )
        field.queryset = TeamMember.objects.all()
        field.required = False
        field.label = "Team Members"
        field.help_text = (
            "Tick the members to show in this section. Add or edit the "
            "available members from Data Management → Team Members."
        )


class AboutUsTeamSectionForm(TeamMemberPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """About Us page — team section editor. Members are picked from
    `data_management.TeamMember`."""

    class Meta:
        model = AboutUsTeamSection
        fields = ["label", "title", "subtitle", "selected_team_members"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Team"}),
            "title": forms.TextInput(attrs={"placeholder": "Main title"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "Short tagline"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "subtitle": "Sub-title",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_team_members_field()


class TeamMemberForm(BootstrapFormMixin, forms.ModelForm):
    """Single `TeamMember` row — name, profile image, designation, email
    URL, view-profile link. Used by Data Management → Team Members'
    bulk modelformset."""

    class Meta:
        model = TeamMember
        fields = [
            "name",
            "profile_image",
            "designation",
            "email_url",
            "view_profile_url",
        ]
        widgets = {
            "profile_image": CleanFileInput(),
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "designation": forms.TextInput(attrs={"placeholder": "e.g. Co-founder"}),
            "email_url": forms.TextInput(attrs={"placeholder": "mailto:name@example.com"}),
            "view_profile_url": forms.URLInput(attrs={"placeholder": "https://linkedin.com/in/…"}),
        }
        labels = {
            "name": "Name",
            "profile_image": "Profile Image",
            "designation": "Designation",
            "email_url": "Email URL",
            "view_profile_url": "View Profile URL",
        }


TeamMemberFormSet = forms.modelformset_factory(
    TeamMember,
    form=TeamMemberForm,
    extra=0,
    can_delete=True,
)


class AboutUsPledgeSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — pledge section editor. Images live on `SectionImage`."""

    class Meta:
        model = AboutUsPledgeSection
        fields = ["label", "title", "description"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Pledge"}),
            "title": forms.TextInput(attrs={"placeholder": "Main title"}),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Pledge text",
            }),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
        }


class AboutUsJourneySectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — journey section editor. Cards live on the inline
    `AboutUsJourneyCardFormSet`."""

    class Meta:
        model = AboutUsJourneySection
        fields = ["label", "title", "subtitle"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Journey"}),
            "title": forms.TextInput(attrs={"placeholder": "Main title"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "Short tagline"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "subtitle": "Sub-title",
        }


class AboutUsJourneyCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AboutUsJourneyCard
        fields = ["image", "title", "description"]
        widgets = {
            "image": CleanFileInput(),
            "title": forms.TextInput(attrs={"placeholder": "e.g. 2020 — Founded"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description of this milestone",
            }),
        }
        labels = {
            "image": "Image",
            "title": "Title",
            "description": "Description",
        }


AboutUsJourneyCardFormSet = forms.inlineformset_factory(
    AboutUsJourneySection,
    AboutUsJourneyCard,
    form=AboutUsJourneyCardForm,
    extra=0,
    can_delete=True,
)


class AboutUsValuesSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — values section editor. Cards live on the inline
    `AboutUsValueCardFormSet`."""

    class Meta:
        model = AboutUsValuesSection
        fields = ["label", "title", "subtitle"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Values"}),
            "title": forms.TextInput(attrs={"placeholder": "Main title"}),
            "subtitle": forms.TextInput(attrs={"placeholder": "Short tagline"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "subtitle": "Sub-title",
        }


class AboutUsValueCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AboutUsValueCard
        fields = ["icon", "label", "note"]
        widgets = {
            "icon": CleanFileInput(),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Integrity"}),
            "note": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short note explaining the value",
            }),
        }
        labels = {"icon": "Icon", "label": "Label", "note": "Note"}


AboutUsValueCardFormSet = forms.inlineformset_factory(
    AboutUsValuesSection,
    AboutUsValueCard,
    form=AboutUsValueCardForm,
    extra=0,
    can_delete=True,
)


class AboutUsFounderSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — founder section editor. Images live on `SectionImage`."""

    class Meta:
        model = AboutUsFounderSection
        fields = [
            "label",
            "founder_name",
            "designation",
            "description",
            "founder_message",
            "button_text",
            "button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short bio/description of the founder",
            }),
            "founder_message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Personal message from the founder",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Meet the Founder"}),
            "founder_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "designation": forms.TextInput(attrs={"placeholder": "e.g. CEO & Co-founder"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Read More"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/about or https://…"}),
        }
        labels = {
            "label": "Label",
            "founder_name": "Founder Name",
            "designation": "Designation",
            "description": "Description",
            "founder_message": "Founder Message",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class AboutUsMissionSectionForm(StatisticPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """About Us page — mission section editor. Stats are picked from the
    central `Statistic` table; images live on `SectionImage`."""

    class Meta:
        model = AboutUsMissionSection
        fields = ["label", "title", "description", "selected_statistics"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about the mission",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Mission"}),
            "title": forms.TextInput(attrs={"placeholder": "Main title"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_statistics_field()


class SchoolsHeroSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Schools page — top hero section editor. Label, title, description,
    two CTA buttons. Images live on `SectionImage`."""

    class Meta:
        model = SchoolsHeroSection
        fields = [
            "label",
            "title",
            "description",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph below the title",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. For Schools"}),
            "title": forms.TextInput(attrs={"placeholder": "Main hero title"}),
            "primary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Get Started"}),
            "primary_button_url": forms.TextInput(attrs={"placeholder": "/signup or https://…"}),
            "secondary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
            "secondary_button_url": forms.TextInput(attrs={"placeholder": "/about or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "primary_button_text": "Primary Button Text",
            "primary_button_url": "Primary Button URL",
            "secondary_button_text": "Secondary Button Text",
            "secondary_button_url": "Secondary Button URL",
        }


class SchoolsHelpSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Schools page — help section editor. Cards live on the inline
    `SchoolsHelpCardFormSet`."""

    class Meta:
        model = SchoolsHelpSection
        fields = ["label", "title"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. How we help"}),
            "title": forms.TextInput(attrs={"placeholder": "Main section title"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
        }


class SchoolsHelpCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SchoolsHelpCard
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Card title"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description",
            }),
        }
        labels = {
            "title": "Title",
            "description": "Description",
        }


SchoolsHelpCardFormSet = forms.inlineformset_factory(
    SchoolsHelpSection,
    SchoolsHelpCard,
    form=SchoolsHelpCardForm,
    extra=0,
    can_delete=True,
)


class SchoolsEmployerSectionForm(EmployerPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """Schools page — employer section editor. The list of available
    employers lives in Data Management; the form just picks which ones
    to display on this page."""

    class Meta:
        model = SchoolsEmployerSection
        fields = [
            "label",
            "title",
            "description",
            "button_text",
            "button_url",
            "selected_employers",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about partner employers",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Top Employers"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. View All"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/employers or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_employers_field()


class SchoolsBenchmarkSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Schools page — benchmark section editor. Cards live on the inline
    `SchoolsBenchmarkCardFormSet`."""

    class Meta:
        model = SchoolsBenchmarkSection
        fields = ["label", "title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about benchmarks",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Benchmarks"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
        }


class SchoolsBenchmarkCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SchoolsBenchmarkCard
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Benchmark title"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description",
            }),
        }
        labels = {
            "title": "Title",
            "description": "Description",
        }


SchoolsBenchmarkCardFormSet = forms.inlineformset_factory(
    SchoolsBenchmarkSection,
    SchoolsBenchmarkCard,
    form=SchoolsBenchmarkCardForm,
    extra=0,
    can_delete=True,
)


class SchoolsSubscribeSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Schools page — subscribe section editor. Form fields live on the
    inline `SchoolsSubscribeFieldFormSet`; images on `SectionImage`."""

    class Meta:
        model = SchoolsSubscribeSection
        fields = [
            "label",
            "title",
            "description",
            "button_text",
            "button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about the subscribe form",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Stay updated"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Subscribe"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/subscribe or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Subscribe Button Text",
            "button_url": "Subscribe Button URL",
        }


class SchoolsSubscribeFieldForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SchoolsSubscribeField
        fields = ["field_name", "placeholder"]
        widgets = {
            "field_name": forms.TextInput(attrs={"placeholder": "e.g. Email"}),
            "placeholder": forms.TextInput(attrs={"placeholder": "e.g. you@example.com"}),
        }
        labels = {
            "field_name": "Field Name",
            "placeholder": "Placeholder",
        }


SchoolsSubscribeFieldFormSet = forms.inlineformset_factory(
    SchoolsSubscribeSection,
    SchoolsSubscribeField,
    form=SchoolsSubscribeFieldForm,
    extra=0,
    can_delete=True,
)


class SchoolsFaqSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Schools page — FAQ section editor. Q&A items live on the inline
    `SchoolsFaqItemFormSet`."""

    class Meta:
        model = SchoolsFaqSection
        fields = ["label", "title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short intro for the FAQ section",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. FAQ"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
        }


class SchoolsFaqItemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SchoolsFaqItem
        fields = ["question", "answer"]
        widgets = {
            "question": forms.TextInput(attrs={"placeholder": "e.g. How does it work?"}),
            "answer": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Answer to the question",
            }),
        }
        labels = {
            "question": "Question",
            "answer": "Answer",
        }


SchoolsFaqItemFormSet = forms.inlineformset_factory(
    SchoolsFaqSection,
    SchoolsFaqItem,
    form=SchoolsFaqItemForm,
    extra=0,
    can_delete=True,
)


class EmployersHeroSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Employers page — top hero section editor. Label, title, description,
    two CTA buttons. Images live on `SectionImage`."""

    class Meta:
        model = EmployersHeroSection
        fields = [
            "label",
            "title",
            "description",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph below the title",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. For Employers"}),
            "title": forms.TextInput(attrs={"placeholder": "Main hero title"}),
            "primary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Post a Job"}),
            "primary_button_url": forms.TextInput(attrs={"placeholder": "/post or https://…"}),
            "secondary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
            "secondary_button_url": forms.TextInput(attrs={"placeholder": "/about or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "primary_button_text": "Primary Button Text",
            "primary_button_url": "Primary Button URL",
            "secondary_button_text": "Secondary Button Text",
            "secondary_button_url": "Secondary Button URL",
        }


class EmployersMissionSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Employers page — mission section editor. Points live on the inline
    `EmployersMissionPointFormSet`; images on `SectionImage`."""

    class Meta:
        model = EmployersMissionSection
        fields = [
            "label",
            "title",
            "description",
            "button_text",
            "button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about the mission",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Mission"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Get Started"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/start or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class EmployersMissionPointForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EmployersMissionPoint
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Mission point text"}),
        }
        labels = {"text": "Point Text"}


EmployersMissionPointFormSet = forms.inlineformset_factory(
    EmployersMissionSection,
    EmployersMissionPoint,
    form=EmployersMissionPointForm,
    extra=0,
    can_delete=True,
)


class EmployersOfferSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Employers page — offer section editor. Cards live on the inline
    `EmployersOfferCardFormSet`."""

    class Meta:
        model = EmployersOfferSection
        fields = ["label", "title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about what you offer",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. What we offer"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
        }


class EmployersOfferCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EmployersOfferCard
        fields = ["icon", "title", "description"]
        widgets = {
            "icon": CleanFileInput(),
            "title": forms.TextInput(attrs={"placeholder": "Card title"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description",
            }),
        }
        labels = {
            "icon": "Icon",
            "title": "Title",
            "description": "Description",
        }


EmployersOfferCardFormSet = forms.inlineformset_factory(
    EmployersOfferSection,
    EmployersOfferCard,
    form=EmployersOfferCardForm,
    extra=0,
    can_delete=True,
)


class EmployersEventsSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Employers page — events section editor. Images live on the inline
    `EmployersEventImageFormSet`."""

    class Meta:
        model = EmployersEventsSection
        fields = [
            "label",
            "title",
            "description",
            "button_text",
            "button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about the events",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Events"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. View All Events"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/events or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class EmployersEventImageForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EmployersEventImage
        fields = ["image"]
        widgets = {"image": CleanFileInput()}
        labels = {"image": "Image"}


EmployersEventImageFormSet = forms.inlineformset_factory(
    EmployersEventsSection,
    EmployersEventImage,
    form=EmployersEventImageForm,
    extra=0,
    can_delete=True,
)


class PartnersHeroSectionForm(StatisticPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """Partners page — top hero section editor. Label, title, description,
    plus a picker that selects which `Statistic` rows to display."""

    class Meta:
        model = PartnersHeroSection
        fields = ["label", "title", "description", "selected_statistics"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph below the title",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Partners"}),
            "title": forms.TextInput(attrs={"placeholder": "Main hero title"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_statistics_field()


class PartnersPartnerSectionForm(EmployerPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """Partners page — partner section editor. Search placeholder + an
    inline list of categories managed via `PartnersCategoryFormSet` + a
    picker that selects which `Employer` rows to display."""

    class Meta:
        model = PartnersPartnerSection
        fields = ["search_placeholder", "explore_button_text", "selected_employers"]
        widgets = {
            "search_placeholder": forms.TextInput(attrs={"placeholder": "e.g. Search partners…"}),
            "explore_button_text": forms.TextInput(attrs={"placeholder": "e.g. Explore"}),
        }
        labels = {
            "search_placeholder": "Search Placeholder",
            "explore_button_text": "Explore Button Text",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_employers_field()


class PartnersCategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PartnersCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Investors"}),
        }
        labels = {"name": "Category Name"}


PartnersCategoryFormSet = forms.inlineformset_factory(
    PartnersPartnerSection,
    PartnersCategory,
    form=PartnersCategoryForm,
    extra=0,
    can_delete=True,
)


class PartnersFamilySectionForm(EmployerPickerMixin, BootstrapFormMixin, forms.ModelForm):
    """Partners page — family section editor. Label/title/description,
    selectable employers, and a Load More CTA (button text + URL)."""

    class Meta:
        model = PartnersFamilySection
        fields = [
            "label",
            "title",
            "description",
            "selected_employers",
            "load_more_button_text",
            "load_more_button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about the partner family",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Our Family"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "load_more_button_text": forms.TextInput(attrs={"placeholder": "e.g. Load More"}),
            "load_more_button_url": forms.TextInput(attrs={"placeholder": "/partners or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "load_more_button_text": "Load More Button Text",
            "load_more_button_url": "Load More Button URL",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_employers_field()


class PartnersReviewSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Partners page — review section editor. Label + title; review cards
    live on the inline `PartnersReviewCardFormSet`."""

    class Meta:
        model = PartnersReviewSection
        fields = ["label", "title"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Reviews"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
        }
        labels = {"label": "Label", "title": "Title"}


class PartnersReviewCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PartnersReviewCard
        fields = ["name", "designation", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "designation": forms.TextInput(attrs={"placeholder": "e.g. CEO, Acme Co."}),
            "message": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Their review/testimonial",
            }),
        }
        labels = {
            "name": "Name",
            "designation": "Designation",
            "message": "Message",
        }


PartnersReviewCardFormSet = forms.inlineformset_factory(
    PartnersReviewSection,
    PartnersReviewCard,
    form=PartnersReviewCardForm,
    extra=0,
    can_delete=True,
)


class PartnersFounderSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Partners page — founder section editor. Label, title, description,
    two CTA buttons (text + URL). Images live on `SectionImage`."""

    class Meta:
        model = PartnersFounderSection
        fields = [
            "label",
            "title",
            "description",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short bio/founder message",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Meet the Founder"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "primary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Read More"}),
            "primary_button_url": forms.TextInput(attrs={"placeholder": "/about or https://…"}),
            "secondary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Contact"}),
            "secondary_button_url": forms.TextInput(attrs={"placeholder": "/contact or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "primary_button_text": "Primary Button Text",
            "primary_button_url": "Primary Button URL",
            "secondary_button_text": "Secondary Button Text",
            "secondary_button_url": "Secondary Button URL",
        }


class EventsHeroSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Events page — top hero section editor. Label, title, description,
    plus two CTA buttons (text + URL)."""

    class Meta:
        model = EventsHeroSection
        fields = [
            "label",
            "title",
            "description",
            "primary_button_text",
            "primary_button_url",
            "secondary_button_text",
            "secondary_button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph below the title",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Events"}),
            "title": forms.TextInput(attrs={"placeholder": "Main hero title"}),
            "primary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Register"}),
            "primary_button_url": forms.TextInput(attrs={"placeholder": "/register or https://…"}),
            "secondary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
            "secondary_button_url": forms.TextInput(attrs={"placeholder": "/about or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "primary_button_text": "Primary Button Text",
            "primary_button_url": "Primary Button URL",
            "secondary_button_text": "Secondary Button Text",
            "secondary_button_url": "Secondary Button URL",
        }


class EventsFeaturedSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Events page — featured section editor. Label, date/time label,
    title, description, category label, and a single CTA button. Images
    live on `SectionImage`."""

    class Meta:
        model = EventsFeaturedSection
        fields = [
            "label",
            "datetime_label",
            "title",
            "description",
            "category_label",
            "button_text",
            "button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short description of the featured event",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Featured Event"}),
            "datetime_label": forms.TextInput(attrs={"placeholder": "e.g. Fri 15 May - 10:00 - 16:00 BST"}),
            "title": forms.TextInput(attrs={"placeholder": "Event title"}),
            "category_label": forms.TextInput(attrs={"placeholder": "e.g. Workshop"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Register"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/register or https://…"}),
        }
        labels = {
            "label": "Label",
            "datetime_label": "Date / Time (e.g. Fri 15 May - 10:00 - 16:00 BST)",
            "title": "Title",
            "description": "Description",
            "category_label": "Category Label",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class EventsUpcomingSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Events page — upcoming section editor. Label + title + the shared
    card button label; categories and cards live on inline formsets."""

    class Meta:
        model = EventsUpcomingSection
        fields = ["label", "title", "card_button_text"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Upcoming"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "card_button_text": forms.TextInput(attrs={"placeholder": "e.g. Book Now"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "card_button_text": "Card Button Text (shared across all cards)",
        }


class EventsUpcomingCategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EventsUpcomingCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Workshops"}),
        }
        labels = {"name": "Category Name"}


EventsUpcomingCategoryFormSet = forms.inlineformset_factory(
    EventsUpcomingSection,
    EventsUpcomingCategory,
    form=EventsUpcomingCategoryForm,
    extra=0,
    can_delete=True,
)


class EventsUpcomingCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EventsUpcomingCard
        fields = [
            "image",
            "label",
            "title",
            "description",
            "years_label",
            "price_label",
            "button_url",
        ]
        widgets = {
            "image": CleanFileInput(),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short description of the event",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Workshop"}),
            "title": forms.TextInput(attrs={"placeholder": "Event title"}),
            "years_label": forms.TextInput(attrs={"placeholder": "e.g. Years 12+"}),
            "price_label": forms.TextInput(attrs={"placeholder": "e.g. Free"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/event or https://…"}),
        }
        labels = {
            "image": "Image",
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "years_label": "Years (e.g. Years 12+)",
            "price_label": "Price (e.g. Free)",
            "button_url": "Button URL",
        }


EventsUpcomingCardFormSet = forms.inlineformset_factory(
    EventsUpcomingSection,
    EventsUpcomingCard,
    form=EventsUpcomingCardForm,
    extra=0,
    can_delete=True,
)


class EventsMissedSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Events page — missed section editor. Label, title, description,
    plus the shared card button label."""

    class Meta:
        model = EventsMissedSection
        fields = ["label", "title", "description", "card_button_text"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph about past events",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Missed Events"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "card_button_text": forms.TextInput(attrs={"placeholder": "e.g. Watch Now"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "card_button_text": "Card Button Text (shared across all cards)",
        }


class EventsMissedCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EventsMissedCard
        fields = ["video", "title", "date_label", "button_url"]
        widgets = {
            "video": CleanFileInput(attrs={"accept": "video/*"}),
            "title": forms.TextInput(attrs={"placeholder": "Event title"}),
            "date_label": forms.TextInput(attrs={"placeholder": "e.g. AUG 2025"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/recap or https://…"}),
        }
        labels = {
            "video": "Video",
            "title": "Title",
            "date_label": "Date (e.g. AUG 2025)",
            "button_url": "Button URL",
        }


EventsMissedCardFormSet = forms.inlineformset_factory(
    EventsMissedSection,
    EventsMissedCard,
    form=EventsMissedCardForm,
    extra=0,
    can_delete=True,
)


class EventsSubmitSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Events page — submit events section editor. Label, title,
    description, and a single CTA button. Images live on `SectionImage`."""

    class Meta:
        model = EventsSubmitSection
        fields = [
            "label",
            "title",
            "description",
            "button_text",
            "button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph inviting submissions",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Submit an Event"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Submit"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/submit or https://…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class InsightHeroSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Insight page — top hero section editor. Label, title, description,
    plus a search placeholder."""

    class Meta:
        model = InsightHeroSection
        fields = ["label", "title", "description", "search_placeholder"]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph below the title",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Insights"}),
            "title": forms.TextInput(attrs={"placeholder": "Main hero title"}),
            "search_placeholder": forms.TextInput(attrs={"placeholder": "e.g. Search articles…"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "search_placeholder": "Search Placeholder",
        }


class InsightFounderSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Insight page — founder section editor. Two labels, a date label,
    title, description, a meta-data line, and a single CTA button.
    Categories live on the inline `InsightFounderCategoryFormSet`; images
    live on `SectionImage`."""

    class Meta:
        model = InsightFounderSection
        fields = [
            "label_1",
            "label_2",
            "date_label",
            "title",
            "description",
            "meta_data",
            "button_text",
            "button_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short article excerpt",
            }),
            "label_1": forms.TextInput(attrs={"placeholder": "e.g. Founder Story"}),
            "label_2": forms.TextInput(attrs={"placeholder": "e.g. Featured"}),
            "date_label": forms.TextInput(attrs={"placeholder": "e.g. 14 APR 2026"}),
            "title": forms.TextInput(attrs={"placeholder": "Article title"}),
            "meta_data": forms.TextInput(attrs={"placeholder": "e.g. By metro · 4 min read"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Read More"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/article or https://…"}),
        }
        labels = {
            "label_1": "Label 1",
            "label_2": "Label 2",
            "date_label": "Date (e.g. 14 APR 2026)",
            "title": "Title",
            "description": "Description",
            "meta_data": "Meta Data (e.g. By metro - 4 min read)",
            "button_text": "Button Text",
            "button_url": "Button URL",
        }


class InsightFounderCategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = InsightFounderCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Leadership"}),
        }
        labels = {"name": "Category Name"}


InsightFounderCategoryFormSet = forms.inlineformset_factory(
    InsightFounderSection,
    InsightFounderCategory,
    form=InsightFounderCategoryForm,
    extra=0,
    can_delete=True,
)


class InsightArticleSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Insight page — article section editor. Title plus the shared card
    button label; cards live on the inline `InsightArticleCardFormSet`."""

    class Meta:
        model = InsightArticleSection
        fields = ["title", "card_button_text"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Latest Articles"}),
            "card_button_text": forms.TextInput(attrs={"placeholder": "e.g. Read Article"}),
        }
        labels = {
            "title": "Title",
            "card_button_text": "Card Button Text (shared across all cards)",
        }


class InsightArticleCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = InsightArticleCard
        fields = [
            "label",
            "image",
            "date_label",
            "title",
            "description",
            "tag",
            "button_url",
        ]
        widgets = {
            "image": CleanFileInput(),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Short article excerpt",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Article"}),
            "date_label": forms.TextInput(attrs={"placeholder": "e.g. 15 APR 2026"}),
            "title": forms.TextInput(attrs={"placeholder": "Article title"}),
            "tag": forms.TextInput(attrs={"placeholder": "e.g. Career"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/article or https://…"}),
        }
        labels = {
            "label": "Label",
            "image": "Image",
            "date_label": "Date (e.g. 15 APR 2026)",
            "title": "Title",
            "description": "Description",
            "tag": "Tag",
            "button_url": "Button URL",
        }


InsightArticleCardFormSet = forms.inlineformset_factory(
    InsightArticleSection,
    InsightArticleCard,
    form=InsightArticleCardForm,
    extra=0,
    can_delete=True,
)


class InsightLaneSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Insight page — "Pick your lane" section editor. Label + title;
    lanes live on the inline `InsightLaneFormSet`."""

    class Meta:
        model = InsightLaneSection
        fields = ["label", "title"]
        widgets = {
            "label": forms.TextInput(attrs={"placeholder": "e.g. Pick your lane"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
        }
        labels = {"label": "Label", "title": "Title"}


class InsightLaneForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = InsightLane
        fields = ["name", "article_count", "url"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Career advice"}),
            "article_count": forms.TextInput(attrs={"placeholder": "e.g. 12 articles"}),
            "url": forms.TextInput(attrs={"placeholder": "/lane or https://…"}),
        }
        labels = {
            "name": "Lane Name",
            "article_count": "Article Count",
            "url": "URL",
        }


InsightLaneFormSet = forms.inlineformset_factory(
    InsightLaneSection,
    InsightLane,
    form=InsightLaneForm,
    extra=0,
    can_delete=True,
)


class InsightSubscribeSectionForm(BootstrapFormMixin, forms.ModelForm):
    """Insight page — subscribe section editor. Label, title, description,
    email input placeholder, subscribe button (text + URL), bottom note.
    Images live on `SectionImage`."""

    class Meta:
        model = InsightSubscribeSection
        fields = [
            "label",
            "title",
            "description",
            "email_placeholder",
            "button_text",
            "button_url",
            "bottom_note",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Short paragraph inviting subscribers",
            }),
            "label": forms.TextInput(attrs={"placeholder": "e.g. Newsletter"}),
            "title": forms.TextInput(attrs={"placeholder": "Section title"}),
            "email_placeholder": forms.TextInput(attrs={"placeholder": "e.g. Your email address"}),
            "button_text": forms.TextInput(attrs={"placeholder": "e.g. Subscribe"}),
            "button_url": forms.TextInput(attrs={"placeholder": "/subscribe or https://…"}),
            "bottom_note": forms.TextInput(attrs={"placeholder": "Small note under the form"}),
        }
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "email_placeholder": "Email Input Placeholder",
            "button_text": "Subscribe Button Text",
            "button_url": "Subscribe Button URL",
            "bottom_note": "Bottom Note",
        }


class AboutSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About / Mission section editor. Images live on `SectionImage`."""

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
        ]
        widgets = {
            "about_section_description": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Paragraph describing the about/mission",
            }),
            "about_section_label": forms.TextInput(attrs={"placeholder": "e.g. About Us"}),
            "about_section_title": forms.TextInput(attrs={"placeholder": "Main title"}),
            "about_section_primary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Learn More"}),
            "about_section_primary_button_url": forms.TextInput(attrs={"placeholder": "/about or https://…"}),
            "about_section_secondary_button_text": forms.TextInput(attrs={"placeholder": "e.g. Contact Us"}),
            "about_section_secondary_button_url": forms.TextInput(attrs={"placeholder": "/contact or https://…"}),
        }
        labels = {
            "about_section_label": "Label",
            "about_section_title": "Title",
            "about_section_description": "Description",
            "about_section_primary_button_text": "Primary Button Text",
            "about_section_primary_button_url": "Primary Button URL",
            "about_section_secondary_button_text": "Secondary Button Text",
            "about_section_secondary_button_url": "Secondary Button URL",
        }
