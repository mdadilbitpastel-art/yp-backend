"""Dashboard views — fully custom CMS, no Django Admin involved.

Each homepage section is a singleton, so there is only one URL per section
and it goes straight to its edit page.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

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
    AboutSectionForm,
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
    NetworkSectionForm,
    NetworkStatFormSet,
    SocialMediaCardFormSet,
    SocialMediaSectionForm,
    TalentPoolSectionForm,
    TestimonialsSectionForm,
)
from .sections import DASHBOARD_MODULES, get_module, module_stats


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



class HeroEditView(LoginRequiredMixin, UpdateView):
    model = HeroSection
    form_class = HeroSectionForm
    template_name = "dashboard/home/hero_form.html"
    success_url = reverse_lazy("dashboard:hero_edit")

    def get_object(self, queryset=None):
        return HeroSection.load()

    def form_valid(self, form):
        messages.success(self.request, "Hero section saved successfully.")
        return super().form_valid(form)


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


class AboutEditView(LoginRequiredMixin, UpdateView):
    model = AboutSection
    form_class = AboutSectionForm
    template_name = "dashboard/home/about_form.html"
    success_url = reverse_lazy("dashboard:about_edit")

    def get_object(self, queryset=None):
        return AboutSection.load()

    def form_valid(self, form):
        messages.success(self.request, "Mission section saved successfully.")
        return super().form_valid(form)


class NetworkEditView(LoginRequiredMixin, UpdateView):
    model = NetworkSection
    form_class = NetworkSectionForm
    template_name = "dashboard/home/network_form.html"
    success_url = reverse_lazy("dashboard:network_edit")

    def get_object(self, queryset=None):
        return NetworkSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "stat_formset",
            NetworkStatFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        stat_formset = NetworkStatFormSet(request.POST, instance=self.object)
        if form.is_valid() and stat_formset.is_valid():
            form.save()
            stat_formset.save()
            messages.success(request, "Network section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, stat_formset=stat_formset)
        )


class TalentPoolEditView(LoginRequiredMixin, UpdateView):
    model = TalentPoolSection
    form_class = TalentPoolSectionForm
    template_name = "dashboard/home/talent_pool_form.html"
    success_url = reverse_lazy("dashboard:talent_pool_edit")

    def get_object(self, queryset=None):
        return TalentPoolSection.load()

    def form_valid(self, form):
        messages.success(self.request, "Talent Pool section saved successfully.")
        return super().form_valid(form)


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


class AppSectionEditView(LoginRequiredMixin, UpdateView):
    model = AppSection
    form_class = AppSectionForm
    template_name = "dashboard/home/app_form.html"
    success_url = reverse_lazy("dashboard:app_edit")

    def get_object(self, queryset=None):
        return AppSection.load()

    def form_valid(self, form):
        messages.success(self.request, "App section saved successfully.")
        return super().form_valid(form)


class TestimonialsEditView(LoginRequiredMixin, UpdateView):
    model = TestimonialsSection
    form_class = TestimonialsSectionForm
    template_name = "dashboard/home/testimonials_form.html"
    success_url = reverse_lazy("dashboard:testimonials_edit")

    def get_object(self, queryset=None):
        return TestimonialsSection.load()

    def form_valid(self, form):
        messages.success(self.request, "Testimonials section saved successfully.")
        return super().form_valid(form)


class SocialMediaEditView(LoginRequiredMixin, UpdateView):
    model = SocialMediaSection
    form_class = SocialMediaSectionForm
    template_name = "dashboard/home/social_media_form.html"
    success_url = reverse_lazy("dashboard:social_media_edit")

    def get_object(self, queryset=None):
        return SocialMediaSection.load()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault(
            "card_formset",
            SocialMediaCardFormSet(instance=self.object),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        card_formset = SocialMediaCardFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and card_formset.is_valid():
            form.save()
            card_formset.save()
            messages.success(request, "Social Media section saved successfully.")
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, card_formset=card_formset)
        )
