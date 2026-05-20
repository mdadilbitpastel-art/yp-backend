"""Dashboard views — fully custom CMS, no Django Admin involved.

Each homepage section is a singleton, so there is only one URL per section
and it goes straight to its edit page.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, QueryDict
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView

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
from employers.models import (
    EmployersEventsSection,
    EmployersHeroSection,
    EmployersMissionSection,
    EmployersOfferSection,
)
from partners.models import (
    PartnersFamilySection,
    PartnersFounderSection,
    PartnersHeroSection,
    PartnersPartnerSection,
    PartnersReviewSection,
)
from events.models import (
    EventsFeaturedSection,
    EventsHeroSection,
    EventsMissedSection,
    EventsSubmitSection,
    EventsUpcomingSection,
)
from insight.models import (
    InsightArticleSection,
    InsightFounderSection,
    InsightHeroSection,
    InsightLaneSection,
    InsightSubscribeSection,
)
from data_management.models import Employer, SocialMediaIcon, Statistic, TeamMember
from schools.models import (
    SchoolsBenchmarkSection,
    SchoolsEmployerSection,
    SchoolsFaqSection,
    SchoolsHelpSection,
    SchoolsHeroSection,
    SchoolsSubscribeSection,
)
from home.models import (
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

from .forms import (
    SectionImageFormSet,
    AboutSectionForm,
    AboutUsCommunityCardFormSet,
    AboutUsCommunitySectionForm,
    AboutUsFounderSectionForm,
    AboutUsHeroSectionForm,
    AboutUsJourneyCardFormSet,
    AboutUsJourneySectionForm,
    AboutUsMissionSectionForm,
    AboutUsPledgeSectionForm,
    AboutUsSocialMediaSectionForm,
    AboutUsTeamSectionForm,
    AboutUsValueCardFormSet,
    AboutUsValuesSectionForm,
    AppSectionForm,
    ApplyCompanyFormSet,
    ApplySectionForm,
    DashboardLoginForm,
    FeatureCardFormSet,
    FeatureSectionForm,
    FooterLinkFormSet,
    FooterSettingsForm,
    HeaderSettingsForm,
    HeaderTabFormSet,
    HeroSectionForm,
    EmployersEventImageFormSet,
    EmployersEventsSectionForm,
    EmployersHeroSectionForm,
    EmployersMissionPointFormSet,
    EmployersMissionSectionForm,
    EmployersOfferCardFormSet,
    EmployersOfferSectionForm,
    PartnersHeroSectionForm,
    NetworkSectionForm,
    StatisticFormSet,
    EmployerFormSet,
    PartnersCategoryFormSet,
    PartnersFamilySectionForm,
    PartnersFounderSectionForm,
    PartnersPartnerSectionForm,
    PartnersReviewCardFormSet,
    PartnersReviewSectionForm,
    EventsHeroSectionForm,
    EventsFeaturedSectionForm,
    EventsUpcomingSectionForm,
    EventsUpcomingCategoryFormSet,
    EventsUpcomingCardFormSet,
    EventsMissedSectionForm,
    EventsMissedCardFormSet,
    EventsSubmitSectionForm,
    InsightArticleCardFormSet,
    InsightArticleSectionForm,
    InsightFounderCategoryFormSet,
    InsightFounderSectionForm,
    InsightHeroSectionForm,
    InsightLaneFormSet,
    InsightLaneSectionForm,
    InsightSubscribeSectionForm,
    SchoolsBenchmarkCardFormSet,
    SchoolsBenchmarkSectionForm,
    SchoolsEmployerSectionForm,
    SchoolsFaqItemFormSet,
    SchoolsFaqSectionForm,
    SchoolsHelpCardFormSet,
    SchoolsHelpSectionForm,
    SchoolsHeroSectionForm,
    SchoolsSubscribeFieldFormSet,
    SchoolsSubscribeSectionForm,
    SocialMediaIconFormSet,
    SocialMediaSectionForm,
    TalentPoolSectionForm,
    TeamMemberFormSet,
    TestimonialsSectionForm,
)
from .sections import DASHBOARD_MODULES, get_module, module_stats


# ---------------------------------------------------------------------------
# Section editor helpers
# ---------------------------------------------------------------------------
class SectionImagesMixin:
    """Wires a `SectionImageFormSet` into a section editor view so the
    section's "Images" card (`_section_images.html`) renders and saves
    correctly.

    Subclasses set `success_message`; views with additional inline
    formsets (e.g. a card list) override `get_extra_formsets` to return
    `[(context_key, formset_class, queryset_attr?), …]` of extra
    formsets bound to the same instance."""

    success_message = "Section saved successfully."

    def _build_images_formset(self, data=None, files=None):
        return SectionImageFormSet(
            data, files, instance=self.object, prefix="images"
        )

    def get_extra_formsets(self, data=None, files=None):
        """Override to yield `(context_key, formset)` pairs for additional
        inline formsets bound to `self.object`."""
        return []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault("images_formset", self._build_images_formset())
        for key, fs in self.get_extra_formsets():
            ctx.setdefault(key, fs)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        images_formset = self._build_images_formset(request.POST, request.FILES)
        extra = list(self.get_extra_formsets(request.POST, request.FILES))
        all_formsets = [images_formset] + [fs for _, fs in extra]
        if form.is_valid() and all(fs.is_valid() for fs in all_formsets):
            self.object = form.save()
            for fs in all_formsets:
                fs.save()
            messages.success(request, self.success_message)
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(
                form=form,
                images_formset=images_formset,
                **dict(extra),
            )
        )


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
class DashboardLoginView(LoginView):
    template_name = "dashboard/auth/login.html"
    authentication_form = DashboardLoginForm
    redirect_authenticated_user = True


class DashboardLogoutView(LogoutView):
    next_page = reverse_lazy("dashboard:login")


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------
class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["module_summaries"] = [
            {**module, **module_stats(module)} for module in DASHBOARD_MODULES
        ]
        return ctx


# ---------------------------------------------------------------------------
# Header Management — single edit page (no per-section breakdown)
# ---------------------------------------------------------------------------
class HeaderEditView(LoginRequiredMixin, UpdateView):
    model = HeaderSettings
    form_class = HeaderSettingsForm
    template_name = "dashboard/header/header_form.html"
    success_url = reverse_lazy("dashboard:header_edit")

    def get_object(self, queryset=None):
        return HeaderSettings.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "tab_formset",
            HeaderTabFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        tab_formset = HeaderTabFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and tab_formset.is_valid():
            form.save()
            tab_formset.save()
            messages.success(request, "Header saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, tab_formset=tab_formset)
        )


# ---------------------------------------------------------------------------
# Footer Management — single edit page (settings + dynamic links list)
# ---------------------------------------------------------------------------
class FooterEditView(LoginRequiredMixin, UpdateView):
    model = FooterSettings
    form_class = FooterSettingsForm
    template_name = "dashboard/footer/footer_form.html"
    success_url = reverse_lazy("dashboard:footer_edit")

    def get_object(self, queryset=None):
        return FooterSettings.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "link_formset",
            FooterLinkFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        link_formset = FooterLinkFormSet(request.POST, instance=self.object)
        if form.is_valid() and link_formset.is_valid():
            form.save()
            link_formset.save()
            messages.success(request, "Footer saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, link_formset=link_formset)
        )


# ---------------------------------------------------------------------------
# Home Management — module landing + per-section edit views
# ---------------------------------------------------------------------------
class HomeModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("home")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


# ---------------------------------------------------------------------------
# About Us Management — module landing + per-section edit views
# ---------------------------------------------------------------------------
class AboutUsModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/about_us/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("about_us")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


# ---------------------------------------------------------------------------
# Schools Management — module landing + per-section edit views
# ---------------------------------------------------------------------------
class SchoolsModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/schools/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("schools")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


class SchoolsHeroEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = SchoolsHeroSection
    form_class = SchoolsHeroSectionForm
    template_name = "dashboard/schools/hero_form.html"
    success_url = reverse_lazy("dashboard:schools_hero_edit")
    success_message = "Schools hero section saved successfully."

    def get_object(self, queryset=None):
        return SchoolsHeroSection.load()


class SchoolsHelpEditView(LoginRequiredMixin, UpdateView):
    model = SchoolsHelpSection
    form_class = SchoolsHelpSectionForm
    template_name = "dashboard/schools/help_form.html"
    success_url = reverse_lazy("dashboard:schools_help_edit")

    def get_object(self, queryset=None):
        return SchoolsHelpSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            SchoolsHelpCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = SchoolsHelpCardFormSet(request.POST, instance=self.object)
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Schools help section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class SchoolsEmployerEditView(LoginRequiredMixin, UpdateView):
    model = SchoolsEmployerSection
    form_class = SchoolsEmployerSectionForm
    template_name = "dashboard/schools/employer_form.html"
    success_url = reverse_lazy("dashboard:schools_employer_edit")

    def get_object(self, queryset=None):
        return SchoolsEmployerSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_employer_ids"] = list(
            self.object.selected_employers.values_list("pk", flat=True)
        )
        ctx["employer_total_count"] = Employer.objects.count()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Schools employer section saved successfully.")
        return super().form_valid(form)


class SchoolsBenchmarkEditView(LoginRequiredMixin, UpdateView):
    model = SchoolsBenchmarkSection
    form_class = SchoolsBenchmarkSectionForm
    template_name = "dashboard/schools/benchmark_form.html"
    success_url = reverse_lazy("dashboard:schools_benchmark_edit")

    def get_object(self, queryset=None):
        return SchoolsBenchmarkSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            SchoolsBenchmarkCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = SchoolsBenchmarkCardFormSet(request.POST, instance=self.object)
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Schools benchmark section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class SchoolsSubscribeEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = SchoolsSubscribeSection
    form_class = SchoolsSubscribeSectionForm
    template_name = "dashboard/schools/subscribe_form.html"
    success_url = reverse_lazy("dashboard:schools_subscribe_edit")
    success_message = "Schools subscribe section saved successfully."

    def get_object(self, queryset=None):
        return SchoolsSubscribeSection.load()

    def get_extra_formsets(self, data=None, files=None):
        return [
            ("field_formset", SchoolsSubscribeFieldFormSet(data, instance=self.object)),
        ]


# ---------------------------------------------------------------------------
# Employers Management — module landing + per-section edit views
# ---------------------------------------------------------------------------
class EmployersModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/employers/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("employers")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


class EmployersHeroEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = EmployersHeroSection
    form_class = EmployersHeroSectionForm
    template_name = "dashboard/employers/hero_form.html"
    success_url = reverse_lazy("dashboard:employers_hero_edit")
    success_message = "Employers hero section saved successfully."

    def get_object(self, queryset=None):
        return EmployersHeroSection.load()


class EmployersMissionEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = EmployersMissionSection
    form_class = EmployersMissionSectionForm
    template_name = "dashboard/employers/mission_form.html"
    success_url = reverse_lazy("dashboard:employers_mission_edit")
    success_message = "Employers mission section saved successfully."

    def get_object(self, queryset=None):
        return EmployersMissionSection.load()

    def get_extra_formsets(self, data=None, files=None):
        return [
            ("point_formset", EmployersMissionPointFormSet(data, instance=self.object)),
        ]


class EmployersEventsEditView(LoginRequiredMixin, UpdateView):
    model = EmployersEventsSection
    form_class = EmployersEventsSectionForm
    template_name = "dashboard/employers/events_form.html"
    success_url = reverse_lazy("dashboard:employers_events_edit")

    def get_object(self, queryset=None):
        return EmployersEventsSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "image_formset",
            EmployersEventImageFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_formset = EmployersEventImageFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and image_formset.is_valid():
            form.save()
            image_formset.save()
            messages.success(request, "Employers events section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, image_formset=image_formset)
        )


class EmployersOfferEditView(LoginRequiredMixin, UpdateView):
    model = EmployersOfferSection
    form_class = EmployersOfferSectionForm
    template_name = "dashboard/employers/offer_form.html"
    success_url = reverse_lazy("dashboard:employers_offer_edit")

    def get_object(self, queryset=None):
        return EmployersOfferSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            EmployersOfferCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = EmployersOfferCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Employers offer section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class EmployersNetworkEditView(LoginRequiredMixin, UpdateView):
    """Employers — network section editor.

    Shares the same `NetworkSection` singleton as Home → Network — so
    statistic selection edited here is reflected on Home and vice versa.
    """

    model = NetworkSection
    form_class = NetworkSectionForm
    template_name = "dashboard/employers/network_form.html"
    success_url = reverse_lazy("dashboard:employers_network_edit")

    def get_object(self, queryset=None):
        return NetworkSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statistics"] = list(Statistic.objects.all().order_by("order", "id"))
        ctx["selected_statistic_ids"] = list(
            self.object.selected_statistics.values_list("pk", flat=True)
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Network section saved successfully.")
        return super().form_valid(form)


class SchoolsFaqEditView(LoginRequiredMixin, UpdateView):
    model = SchoolsFaqSection
    form_class = SchoolsFaqSectionForm
    template_name = "dashboard/schools/faq_form.html"
    success_url = reverse_lazy("dashboard:schools_faq_edit")

    def get_object(self, queryset=None):
        return SchoolsFaqSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "item_formset",
            SchoolsFaqItemFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        item_formset = SchoolsFaqItemFormSet(request.POST, instance=self.object)
        if form.is_valid() and item_formset.is_valid():
            form.save()
            item_formset.save()
            messages.success(request, "Schools FAQ section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, item_formset=item_formset)
        )


class AboutUsHeroEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = AboutUsHeroSection
    form_class = AboutUsHeroSectionForm
    template_name = "dashboard/about_us/hero_form.html"
    success_url = reverse_lazy("dashboard:about_us_hero_edit")
    success_message = "About Us hero section saved successfully."

    def get_object(self, queryset=None):
        return AboutUsHeroSection.load()


class AboutUsSocialMediaEditView(LoginRequiredMixin, UpdateView):
    """About Us — social media editor. Label/heading/sub-title plus its
    own selection of icons from Data Management → Social Media."""

    model = AboutUsSocialMediaSection
    form_class = AboutUsSocialMediaSectionForm
    template_name = "dashboard/about_us/social_media_form.html"
    success_url = reverse_lazy("dashboard:about_us_social_media_edit")

    def get_object(self, queryset=None):
        return AboutUsSocialMediaSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["social_icons"] = list(
            SocialMediaIcon.objects.all().order_by("order", "id")
        )
        ctx["selected_social_media_ids"] = list(
            self.object.selected_social_media.values_list("pk", flat=True)
        )
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, "About Us social media section saved successfully."
        )
        return super().form_valid(form)


class AboutUsCommunityEditView(LoginRequiredMixin, UpdateView):
    model = AboutUsCommunitySection
    form_class = AboutUsCommunitySectionForm
    template_name = "dashboard/about_us/community_form.html"
    success_url = reverse_lazy("dashboard:about_us_community_edit")

    def get_object(self, queryset=None):
        return AboutUsCommunitySection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            AboutUsCommunityCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = AboutUsCommunityCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "About Us community section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class AboutUsTeamEditView(LoginRequiredMixin, UpdateView):
    model = AboutUsTeamSection
    form_class = AboutUsTeamSectionForm
    template_name = "dashboard/about_us/team_form.html"
    success_url = reverse_lazy("dashboard:about_us_team_edit")

    def get_object(self, queryset=None):
        return AboutUsTeamSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_team_member_ids"] = list(
            self.object.selected_team_members.values_list("pk", flat=True)
        )
        ctx["team_total_count"] = TeamMember.objects.count()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "About Us team section saved successfully.")
        return super().form_valid(form)


class AboutUsPledgeEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = AboutUsPledgeSection
    form_class = AboutUsPledgeSectionForm
    template_name = "dashboard/about_us/pledge_form.html"
    success_url = reverse_lazy("dashboard:about_us_pledge_edit")
    success_message = "About Us pledge section saved successfully."

    def get_object(self, queryset=None):
        return AboutUsPledgeSection.load()


class AboutUsJourneyEditView(LoginRequiredMixin, UpdateView):
    model = AboutUsJourneySection
    form_class = AboutUsJourneySectionForm
    template_name = "dashboard/about_us/journey_form.html"
    success_url = reverse_lazy("dashboard:about_us_journey_edit")

    def get_object(self, queryset=None):
        return AboutUsJourneySection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            AboutUsJourneyCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = AboutUsJourneyCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "About Us journey section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class AboutUsValuesEditView(LoginRequiredMixin, UpdateView):
    model = AboutUsValuesSection
    form_class = AboutUsValuesSectionForm
    template_name = "dashboard/about_us/values_form.html"
    success_url = reverse_lazy("dashboard:about_us_values_edit")

    def get_object(self, queryset=None):
        return AboutUsValuesSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            AboutUsValueCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = AboutUsValueCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "About Us values section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class AboutUsFounderEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = AboutUsFounderSection
    form_class = AboutUsFounderSectionForm
    template_name = "dashboard/about_us/founder_form.html"
    success_url = reverse_lazy("dashboard:about_us_founder_edit")
    success_message = "About Us founder section saved successfully."

    def get_object(self, queryset=None):
        return AboutUsFounderSection.load()


class AboutUsMissionEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    """Mission section editor — statistics picker + section images list."""

    model = AboutUsMissionSection
    form_class = AboutUsMissionSectionForm
    template_name = "dashboard/about_us/mission_form.html"
    success_url = reverse_lazy("dashboard:about_us_mission_edit")
    success_message = "About Us mission section saved successfully."

    def get_object(self, queryset=None):
        return AboutUsMissionSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statistics"] = list(Statistic.objects.all().order_by("order", "id"))
        ctx["selected_statistic_ids"] = list(
            self.object.selected_statistics.values_list("pk", flat=True)
        )
        return ctx



class HeroEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = HeroSection
    form_class = HeroSectionForm
    template_name = "dashboard/home/hero_form.html"
    success_url = reverse_lazy("dashboard:hero_edit")
    success_message = "Hero section saved successfully."

    def get_object(self, queryset=None):
        return HeroSection.load()


class FeatureEditView(LoginRequiredMixin, UpdateView):
    model = FeatureSection
    form_class = FeatureSectionForm
    template_name = "dashboard/home/feature_form.html"
    success_url = reverse_lazy("dashboard:feature_edit")

    def get_object(self, queryset=None):
        return FeatureSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            FeatureCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = FeatureCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Feature section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class AboutEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = AboutSection
    form_class = AboutSectionForm
    template_name = "dashboard/home/about_form.html"
    success_url = reverse_lazy("dashboard:about_edit")
    success_message = "Mission section saved successfully."

    def get_object(self, queryset=None):
        return AboutSection.load()


class NetworkEditView(LoginRequiredMixin, UpdateView):
    model = NetworkSection
    form_class = NetworkSectionForm
    template_name = "dashboard/home/network_form.html"
    success_url = reverse_lazy("dashboard:network_edit")

    def get_object(self, queryset=None):
        return NetworkSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statistics"] = list(Statistic.objects.all().order_by("order", "id"))
        ctx["selected_statistic_ids"] = list(
            self.object.selected_statistics.values_list("pk", flat=True)
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Network section saved successfully.")
        return super().form_valid(form)


class TalentPoolEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = TalentPoolSection
    form_class = TalentPoolSectionForm
    template_name = "dashboard/home/talent_pool_form.html"
    success_url = reverse_lazy("dashboard:talent_pool_edit")
    success_message = "Talent Pool section saved successfully."

    def get_object(self, queryset=None):
        return TalentPoolSection.load()


class ApplyEditView(LoginRequiredMixin, UpdateView):
    model = ApplySection
    form_class = ApplySectionForm
    template_name = "dashboard/home/apply_form.html"
    success_url = reverse_lazy("dashboard:apply_edit")

    def get_object(self, queryset=None):
        return ApplySection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "company_formset",
            ApplyCompanyFormSet(instance=self.object),
        )
        ctx["selected_employer_ids"] = list(
            self.object.selected_employers.values_list("pk", flat=True)
        )
        ctx["employer_total_count"] = Employer.objects.count()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        company_formset = ApplyCompanyFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and company_formset.is_valid():
            form.save()
            company_formset.save()
            messages.success(request, "Apply section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, company_formset=company_formset)
        )


class AppSectionEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = AppSection
    form_class = AppSectionForm
    template_name = "dashboard/home/app_form.html"
    success_url = reverse_lazy("dashboard:app_edit")
    success_message = "App section saved successfully."

    def get_object(self, queryset=None):
        return AppSection.load()


class TestimonialsEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = TestimonialsSection
    form_class = TestimonialsSectionForm
    template_name = "dashboard/home/testimonials_form.html"
    success_url = reverse_lazy("dashboard:testimonials_edit")
    success_message = "Testimonials section saved successfully."

    def get_object(self, queryset=None):
        return TestimonialsSection.load()

    def get_context_data(self, **kwargs):
        from home.models import TestimonialUser

        ctx = super().get_context_data(**kwargs)
        rows = (
            TestimonialUser.objects.filter(section=self.object)
            .exclude(team_member__isnull=True)
            .values("team_member_id", "message")
        )
        ctx["selected_team_member_ids"] = [r["team_member_id"] for r in rows]
        ctx["existing_team_member_messages"] = {
            r["team_member_id"]: r["message"] for r in rows
        }
        ctx["team_total_count"] = TeamMember.objects.count()
        return ctx


class SocialMediaEditView(LoginRequiredMixin, UpdateView):
    model = SocialMediaSection
    form_class = SocialMediaSectionForm
    template_name = "dashboard/home/social_media_form.html"
    success_url = reverse_lazy("dashboard:social_media_edit")

    def get_object(self, queryset=None):
        return SocialMediaSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["social_icons"] = list(
            SocialMediaIcon.objects.all().order_by("order", "id")
        )
        ctx["selected_social_media_ids"] = list(
            self.object.selected_social_media.values_list("pk", flat=True)
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Social Media section saved successfully.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Partner Management — module landing + per-section edit views
# ---------------------------------------------------------------------------
class PartnersModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/partners/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("partners")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


class PartnersHeroEditView(LoginRequiredMixin, UpdateView):
    model = PartnersHeroSection
    form_class = PartnersHeroSectionForm
    template_name = "dashboard/partners/hero_form.html"
    success_url = reverse_lazy("dashboard:partners_hero_edit")

    def get_object(self, queryset=None):
        return PartnersHeroSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statistics"] = list(Statistic.objects.all().order_by("order", "id"))
        ctx["selected_statistic_ids"] = list(
            self.object.selected_statistics.values_list("pk", flat=True)
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Partners hero section saved successfully.")
        return super().form_valid(form)


class PartnersPartnerSectionEditView(LoginRequiredMixin, UpdateView):
    model = PartnersPartnerSection
    form_class = PartnersPartnerSectionForm
    template_name = "dashboard/partners/partner_section_form.html"
    success_url = reverse_lazy("dashboard:partners_partner_section_edit")

    def get_object(self, queryset=None):
        return PartnersPartnerSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "category_formset",
            PartnersCategoryFormSet(instance=self.object),
        )
        ctx["selected_employer_ids"] = list(
            self.object.selected_employers.values_list("pk", flat=True)
        )
        ctx["employer_total_count"] = Employer.objects.count()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        category_formset = PartnersCategoryFormSet(
            request.POST, instance=self.object
        )
        if form.is_valid() and category_formset.is_valid():
            form.save()
            category_formset.save()
            messages.success(request, "Partners partner section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, category_formset=category_formset)
        )


class PartnersFamilySectionEditView(LoginRequiredMixin, UpdateView):
    model = PartnersFamilySection
    form_class = PartnersFamilySectionForm
    template_name = "dashboard/partners/family_section_form.html"
    success_url = reverse_lazy("dashboard:partners_family_section_edit")

    def get_object(self, queryset=None):
        return PartnersFamilySection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_employer_ids"] = list(
            self.object.selected_employers.values_list("pk", flat=True)
        )
        ctx["employer_total_count"] = Employer.objects.count()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Partners family section saved successfully.")
        return super().form_valid(form)


class PartnersReviewSectionEditView(LoginRequiredMixin, UpdateView):
    model = PartnersReviewSection
    form_class = PartnersReviewSectionForm
    template_name = "dashboard/partners/review_section_form.html"
    success_url = reverse_lazy("dashboard:partners_review_section_edit")

    def get_object(self, queryset=None):
        return PartnersReviewSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            PartnersReviewCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = PartnersReviewCardFormSet(
            request.POST, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Partners review section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class PartnersFounderSectionEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = PartnersFounderSection
    form_class = PartnersFounderSectionForm
    template_name = "dashboard/partners/founder_section_form.html"
    success_url = reverse_lazy("dashboard:partners_founder_section_edit")
    success_message = "Partners founder section saved successfully."

    def get_object(self, queryset=None):
        return PartnersFounderSection.load()


# ---------------------------------------------------------------------------
# Events Management — module landing + per-section edit views
# ---------------------------------------------------------------------------
class EventsModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/events/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("events")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


class EventsHeroEditView(LoginRequiredMixin, UpdateView):
    model = EventsHeroSection
    form_class = EventsHeroSectionForm
    template_name = "dashboard/events/hero_form.html"
    success_url = reverse_lazy("dashboard:events_hero_edit")

    def get_object(self, queryset=None):
        return EventsHeroSection.load()

    def form_valid(self, form):
        messages.success(self.request, "Events hero section saved successfully.")
        return super().form_valid(form)


class EventsFeaturedEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = EventsFeaturedSection
    form_class = EventsFeaturedSectionForm
    template_name = "dashboard/events/featured_section_form.html"
    success_url = reverse_lazy("dashboard:events_featured_edit")
    success_message = "Events featured section saved successfully."

    def get_object(self, queryset=None):
        return EventsFeaturedSection.load()


class EventsUpcomingEditView(LoginRequiredMixin, UpdateView):
    model = EventsUpcomingSection
    form_class = EventsUpcomingSectionForm
    template_name = "dashboard/events/upcoming_section_form.html"
    success_url = reverse_lazy("dashboard:events_upcoming_edit")

    def get_object(self, queryset=None):
        return EventsUpcomingSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "category_formset",
            EventsUpcomingCategoryFormSet(instance=self.object, prefix="categories"),
        )
        ctx.setdefault(
            "card_formset",
            EventsUpcomingCardFormSet(instance=self.object, prefix="cards"),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        category_formset = EventsUpcomingCategoryFormSet(
            request.POST, instance=self.object, prefix="categories"
        )
        card_formset = EventsUpcomingCardFormSet(
            request.POST, request.FILES, instance=self.object, prefix="cards"
        )
        if (
            form.is_valid()
            and category_formset.is_valid()
            and card_formset.is_valid()
        ):
            form.save()
            category_formset.save()
            card_formset.save()
            messages.success(request, "Events upcoming section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(
                form=form,
                category_formset=category_formset,
                card_formset=card_formset,
            )
        )


class EventsMissedEditView(LoginRequiredMixin, UpdateView):
    model = EventsMissedSection
    form_class = EventsMissedSectionForm
    template_name = "dashboard/events/missed_section_form.html"
    success_url = reverse_lazy("dashboard:events_missed_edit")

    def get_object(self, queryset=None):
        return EventsMissedSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            EventsMissedCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = EventsMissedCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Events missed section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class EventsSubmitEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = EventsSubmitSection
    form_class = EventsSubmitSectionForm
    template_name = "dashboard/events/submit_section_form.html"
    success_url = reverse_lazy("dashboard:events_submit_edit")
    success_message = "Events submit section saved successfully."

    def get_object(self, queryset=None):
        return EventsSubmitSection.load()


# ---------------------------------------------------------------------------
# Insight Management — module landing + per-section edit views
# ---------------------------------------------------------------------------
class InsightModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/insight/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("insight")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


class InsightHeroEditView(LoginRequiredMixin, UpdateView):
    model = InsightHeroSection
    form_class = InsightHeroSectionForm
    template_name = "dashboard/insight/hero_form.html"
    success_url = reverse_lazy("dashboard:insight_hero_edit")

    def get_object(self, queryset=None):
        return InsightHeroSection.load()

    def form_valid(self, form):
        messages.success(self.request, "Insight hero section saved successfully.")
        return super().form_valid(form)


class InsightFounderSectionEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = InsightFounderSection
    form_class = InsightFounderSectionForm
    template_name = "dashboard/insight/founder_section_form.html"
    success_url = reverse_lazy("dashboard:insight_founder_section_edit")
    success_message = "Insight founder section saved successfully."

    def get_object(self, queryset=None):
        return InsightFounderSection.load()

    def get_extra_formsets(self, data=None, files=None):
        return [
            (
                "category_formset",
                InsightFounderCategoryFormSet(data, instance=self.object),
            ),
        ]


class InsightArticleSectionEditView(LoginRequiredMixin, UpdateView):
    model = InsightArticleSection
    form_class = InsightArticleSectionForm
    template_name = "dashboard/insight/article_section_form.html"
    success_url = reverse_lazy("dashboard:insight_article_section_edit")

    def get_object(self, queryset=None):
        return InsightArticleSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            InsightArticleCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = InsightArticleCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Insight article section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )


class InsightLaneSectionEditView(LoginRequiredMixin, UpdateView):
    model = InsightLaneSection
    form_class = InsightLaneSectionForm
    template_name = "dashboard/insight/lane_section_form.html"
    success_url = reverse_lazy("dashboard:insight_lane_section_edit")

    def get_object(self, queryset=None):
        return InsightLaneSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "lane_formset",
            InsightLaneFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        lane_formset = InsightLaneFormSet(request.POST, instance=self.object)
        if form.is_valid() and lane_formset.is_valid():
            form.save()
            lane_formset.save()
            messages.success(request, "Insight lane section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, lane_formset=lane_formset)
        )


class InsightSubscribeSectionEditView(SectionImagesMixin, LoginRequiredMixin, UpdateView):
    model = InsightSubscribeSection
    form_class = InsightSubscribeSectionForm
    template_name = "dashboard/insight/subscribe_section_form.html"
    success_url = reverse_lazy("dashboard:insight_subscribe_section_edit")
    success_message = "Insight subscribe section saved successfully."

    def get_object(self, queryset=None):
        return InsightSubscribeSection.load()


# ---------------------------------------------------------------------------
# Data Management — shared dynamic data, currently just `Statistic` rows.
# ---------------------------------------------------------------------------
class DataModuleView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/data/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = get_module("data")
        stats = module_stats(module)
        ctx["module"] = module
        ctx["sections"] = stats["sections"]
        ctx["stats"] = stats
        return ctx


class StatisticsEditView(LoginRequiredMixin, TemplateView):
    """Bulk editor for all `Statistic` rows — add / edit / delete via a
    single modelformset. Each row becomes selectable in the Network /
    Mission / Partners-Hero pickers."""

    template_name = "dashboard/data/statistics_form.html"
    success_url = reverse_lazy("dashboard:statistics_edit")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "formset",
            StatisticFormSet(queryset=Statistic.objects.all()),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        formset = StatisticFormSet(request.POST, queryset=Statistic.objects.all())
        if formset.is_valid():
            formset.save()
            messages.success(request, "Statistics saved successfully.")
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(formset=formset))


class EmployersEditView(LoginRequiredMixin, TemplateView):
    """Bulk editor for all `Employer` rows — add / edit / delete via a
    single modelformset. Each row becomes selectable in the Schools
    Employer Section picker."""

    template_name = "dashboard/data/employers_form.html"
    success_url = reverse_lazy("dashboard:employers_edit")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "formset",
            EmployerFormSet(queryset=Employer.objects.all()),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        formset = EmployerFormSet(
            request.POST, request.FILES, queryset=Employer.objects.all()
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "Employers saved successfully.")
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(formset=formset))


class TeamMembersEditView(LoginRequiredMixin, TemplateView):
    """Bulk editor for `TeamMember` rows — add / edit / delete via a
    paginated modelformset with name/designation search. Each row becomes
    selectable in the About Us Team Section picker."""

    template_name = "dashboard/data/team_members_form.html"
    page_size = 10

    def _filtered_queryset(self, query):
        qs = TeamMember.objects.all().order_by("order", "id")
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(designation__icontains=query)
                | Q(email_url__icontains=query)
            )
        return qs

    def _page_queryset(self, source, query):
        qs = self._filtered_queryset(query)
        paginator = Paginator(qs, self.page_size)
        page = paginator.get_page(source.get("page"))
        page_qs = qs.filter(pk__in=[obj.pk for obj in page.object_list])
        return page, page_qs

    def _success_redirect(self, query, page_number):
        params = QueryDict(mutable=True)
        if query:
            params["q"] = query
        if page_number:
            params["page"] = str(page_number)
        url = reverse_lazy("dashboard:team_members_edit")
        return redirect(f"{url}?{params.urlencode()}" if params else url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        page, page_qs = self._page_queryset(self.request.GET, query)
        ctx.setdefault("formset", TeamMemberFormSet(queryset=page_qs))
        ctx["page_obj"] = page
        ctx["paginator"] = page.paginator
        ctx["search_query"] = query
        ctx["total_count"] = page.paginator.count
        return ctx

    def post(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        page, page_qs = self._page_queryset(request.GET, query)
        formset = TeamMemberFormSet(
            request.POST, request.FILES, queryset=page_qs
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "Team members saved successfully.")
            return self._success_redirect(query, page.number)
        ctx = self.get_context_data(formset=formset)
        ctx["page_obj"] = page
        ctx["paginator"] = page.paginator
        ctx["search_query"] = query
        ctx["total_count"] = page.paginator.count
        return self.render_to_response(ctx)


class TeamMemberPickerAPIView(LoginRequiredMixin, View):
    """JSON endpoint that powers the paginated, searchable team-member
    picker on the About Us → Team Section page. Returns:

        {
          "members": [{"id", "name", "designation", "profile_image"}],
          "page": N, "num_pages": N, "total": N, "page_size": N
        }
    """

    page_size = 10
    max_page_size = 50

    def get(self, request, *args, **kwargs):
        from django.db.models import Case, IntegerField, Value, When

        query = request.GET.get("q", "").strip()
        selected_raw = request.GET.get("selected_ids", "")
        selected_ids = [int(x) for x in selected_raw.split(",") if x.isdigit()]
        page_size = self.page_size
        try:
            requested = int(request.GET.get("page_size", ""))
            if 1 <= requested <= self.max_page_size:
                page_size = requested
        except (TypeError, ValueError):
            pass

        qs = TeamMember.objects.all()
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(designation__icontains=query)
                | Q(email_url__icontains=query)
            )

        if selected_ids:
            qs = qs.annotate(
                _is_selected=Case(
                    When(pk__in=selected_ids, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            ).order_by("_is_selected", "order", "id")
        else:
            qs = qs.order_by("order", "id")

        paginator = Paginator(qs, page_size)
        page = paginator.get_page(request.GET.get("page"))
        members = []
        for m in page.object_list:
            members.append({
                "id": m.pk,
                "name": m.name,
                "designation": m.designation,
                "profile_image": m.profile_image.url if m.profile_image else "",
            })
        return JsonResponse({
            "members": members,
            "page": page.number,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
            "page_size": page_size,
        })


class EmployerPickerAPIView(LoginRequiredMixin, View):
    """JSON endpoint that powers the paginated, searchable employer
    picker on the Schools → Employer Section page. Returns:

        {
          "employers": [{"id", "name", "logo"}],
          "page": N, "num_pages": N, "total": N, "page_size": N
        }
    """

    page_size = 10

    def get(self, request, *args, **kwargs):
        from django.db.models import Case, IntegerField, Value, When

        query = request.GET.get("q", "").strip()
        selected_raw = request.GET.get("selected_ids", "")
        selected_ids = [int(x) for x in selected_raw.split(",") if x.isdigit()]

        qs = Employer.objects.all()
        if query:
            qs = qs.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        if selected_ids:
            qs = qs.annotate(
                _is_selected=Case(
                    When(pk__in=selected_ids, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            ).order_by("_is_selected", "order", "id")
        else:
            qs = qs.order_by("order", "id")

        paginator = Paginator(qs, self.page_size)
        page = paginator.get_page(request.GET.get("page"))
        employers = []
        for e in page.object_list:
            employers.append({
                "id": e.pk,
                "name": e.name,
                "logo": e.logo.url if e.logo else "",
            })
        return JsonResponse({
            "employers": employers,
            "page": page.number,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
            "page_size": self.page_size,
        })


class SocialMediaIconsEditView(LoginRequiredMixin, TemplateView):
    """Bulk editor for all `SocialMediaIcon` rows — add / edit / delete
    via a single modelformset. Each row becomes selectable in the Home
    and About Us Social Media section pickers."""

    template_name = "dashboard/data/social_media_form.html"
    success_url = reverse_lazy("dashboard:social_media_icons_edit")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "formset",
            SocialMediaIconFormSet(queryset=SocialMediaIcon.objects.all()),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        formset = SocialMediaIconFormSet(
            request.POST, request.FILES, queryset=SocialMediaIcon.objects.all()
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "Social media icons saved successfully.")
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(formset=formset))
