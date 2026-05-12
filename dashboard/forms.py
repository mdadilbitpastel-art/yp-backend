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
    AboutUsTeamMember,
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
from data_management.models import Employer, SectionImage, SocialMediaIcon, Statistic
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
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
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
        }
        labels = {
            "network_section_title": "Title",
            "network_section_video": "Video",
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
            "description": forms.Textarea(attrs={"rows": 3}),
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
            "apply_section_bottom_button_text": "Button Text",
            "apply_section_bottom_button_url": "Button URL",
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
            "talent_pool_section_description": forms.Textarea(attrs={"rows": 5}),
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
        widgets = {"icon": CleanFileInput()}
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
        labels = {"title": "Title"}


class TestimonialUserForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TestimonialUser
        fields = ["name", "profile_image", "message"]
        widgets = {
            "profile_image": CleanFileInput(),
            "message": forms.Textarea(attrs={"rows": 3}),
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
    """App section editor — title, description, 3 buttons. Images (side +
    barcode) live on `SectionImage`."""

    class Meta:
        model = AppSection
        fields = [
            "title",
            "description",
            *_app_button_field_names(),
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "title": "Title",
            "description": "Description",
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
            "description": forms.Textarea(attrs={"rows": 3}),
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


class AboutUsTeamSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — team section editor. Members live on the inline
    `AboutUsTeamMemberFormSet`."""

    class Meta:
        model = AboutUsTeamSection
        fields = ["label", "title", "subtitle"]
        labels = {
            "label": "Label",
            "title": "Title",
            "subtitle": "Sub-title",
        }


class AboutUsTeamMemberForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AboutUsTeamMember
        fields = [
            "profile_image",
            "name",
            "designation",
            "email_icon",
            "email_url",
            "view_profile_text",
            "view_profile_url",
        ]
        widgets = {
            "profile_image": CleanFileInput(),
            "email_icon": CleanFileInput(),
        }
        labels = {
            "profile_image": "Profile Image",
            "name": "Name",
            "designation": "Designation",
            "email_icon": "Email Icon",
            "email_url": "Email URL",
            "view_profile_text": "View Profile Link Text",
            "view_profile_url": "View Profile URL",
        }


AboutUsTeamMemberFormSet = forms.inlineformset_factory(
    AboutUsTeamSection,
    AboutUsTeamMember,
    form=AboutUsTeamMemberForm,
    extra=0,
    can_delete=True,
)


class AboutUsPledgeSectionForm(BootstrapFormMixin, forms.ModelForm):
    """About Us page — pledge section editor. Images live on `SectionImage`."""

    class Meta:
        model = AboutUsPledgeSection
        fields = ["label", "title", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
            "description": forms.Textarea(attrs={"rows": 3}),
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
            "note": forms.Textarea(attrs={"rows": 3}),
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
            "description": forms.Textarea(attrs={"rows": 4}),
            "founder_message": forms.Textarea(attrs={"rows": 4}),
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
        labels = {
            "label": "Label",
            "title": "Title",
        }


class SchoolsHelpCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SchoolsHelpCard
        fields = ["title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
            "description": forms.Textarea(attrs={"rows": 3}),
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
            "answer": forms.Textarea(attrs={"rows": 3}),
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
            "description": forms.Textarea(attrs={"rows": 3}),
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
        labels = {"label": "Label", "title": "Title"}


class PartnersReviewCardForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PartnersReviewCard
        fields = ["name", "designation", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 3})}
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
            "description": forms.Textarea(attrs={"rows": 4}),
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
        labels = {
            "label": "Label",
            "title": "Title",
            "card_button_text": "Card Button Text (shared across all cards)",
        }


class EventsUpcomingCategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EventsUpcomingCategory
        fields = ["name"]
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
            "description": forms.Textarea(attrs={"rows": 3}),
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
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
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
        labels = {
            "label": "Label",
            "title": "Title",
            "description": "Description",
            "button_text": "Button Text",
            "button_url": "Button URL",
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
            "about_section_description": forms.Textarea(attrs={"rows": 5}),
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
