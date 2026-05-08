"""Dashboard URL routing — all paths live under /dashboard/."""

from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    # Auth
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", views.DashboardLogoutView.as_view(), name="logout"),

    # Index
    path("", views.DashboardIndexView.as_view(), name="index"),

    # Header Management
    path("header/", views.HeaderEditView.as_view(), name="header_edit"),

    # Footer Management
    path("footer/", views.FooterEditView.as_view(), name="footer_edit"),

    # Home Management
    path("home/", views.HomeModuleView.as_view(), name="home_module"),
    path("home/hero/", views.HeroEditView.as_view(), name="hero_edit"),
    path("home/features/", views.FeatureEditView.as_view(), name="feature_edit"),
    path("home/about/", views.AboutEditView.as_view(), name="about_edit"),
    path("home/network/", views.NetworkEditView.as_view(), name="network_edit"),
    path("home/talent-pool/", views.TalentPoolEditView.as_view(), name="talent_pool_edit"),
    path("home/apply/", views.ApplyEditView.as_view(), name="apply_edit"),
    path("home/social-media/", views.SocialMediaEditView.as_view(), name="social_media_edit"),
    path("home/testimonials/", views.TestimonialsEditView.as_view(), name="testimonials_edit"),
    path("home/app/", views.AppSectionEditView.as_view(), name="app_edit"),

    # About Us Management
    path("about-us/", views.AboutUsModuleView.as_view(), name="about_us_module"),
    path("about-us/hero/", views.AboutUsHeroEditView.as_view(), name="about_us_hero_edit"),
    path("about-us/mission/", views.AboutUsMissionEditView.as_view(), name="about_us_mission_edit"),
    path("about-us/founder/", views.AboutUsFounderEditView.as_view(), name="about_us_founder_edit"),
    path("about-us/values/", views.AboutUsValuesEditView.as_view(), name="about_us_values_edit"),
    path("about-us/journey/", views.AboutUsJourneyEditView.as_view(), name="about_us_journey_edit"),
    path("about-us/pledge/", views.AboutUsPledgeEditView.as_view(), name="about_us_pledge_edit"),
    path("about-us/team/", views.AboutUsTeamEditView.as_view(), name="about_us_team_edit"),
    path("about-us/community/", views.AboutUsCommunityEditView.as_view(), name="about_us_community_edit"),
    path("about-us/social-media/", views.AboutUsSocialMediaEditView.as_view(), name="about_us_social_media_edit"),

    # Schools Management
    path("schools/", views.SchoolsModuleView.as_view(), name="schools_module"),
    path("schools/hero/", views.SchoolsHeroEditView.as_view(), name="schools_hero_edit"),
    path("schools/help/", views.SchoolsHelpEditView.as_view(), name="schools_help_edit"),
    path("schools/employer/", views.SchoolsEmployerEditView.as_view(), name="schools_employer_edit"),
    path("schools/benchmark/", views.SchoolsBenchmarkEditView.as_view(), name="schools_benchmark_edit"),
    path("schools/subscribe/", views.SchoolsSubscribeEditView.as_view(), name="schools_subscribe_edit"),
    path("schools/faq/", views.SchoolsFaqEditView.as_view(), name="schools_faq_edit"),

    # Employers Management
    path("employers/", views.EmployersModuleView.as_view(), name="employers_module"),
    path("employers/hero/", views.EmployersHeroEditView.as_view(), name="employers_hero_edit"),
    path("employers/network/", views.EmployersNetworkEditView.as_view(), name="employers_network_edit"),
    path("employers/mission/", views.EmployersMissionEditView.as_view(), name="employers_mission_edit"),
    path("employers/offer/", views.EmployersOfferEditView.as_view(), name="employers_offer_edit"),
    path("employers/events/", views.EmployersEventsEditView.as_view(), name="employers_events_edit"),
]
