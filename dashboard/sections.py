"""Central registry of dashboard modules and their sections.

Adding a new section here makes it appear in:
- the sidebar (under its module group),
- the module landing page (e.g. /dashboard/home/),
- the dashboard overview's module summary card.

Each section now owns its own singleton model, so each entry carries its
own `loader` path. `primary_field` is checked on that loaded singleton to
decide whether the section is already configured — used for the
"x of y configured" stat.
"""


DASHBOARD_MODULES = [
    {
        "key": "header",
        "title": "Header Management",
        "icon": "fas fa-window-maximize",
        "description": "Site-wide header — logo, CTA button, and a manual list of navigation tabs.",
        "flat": True,
        "index_url": "dashboard:header_edit",
        "loader": "home.models.HeaderSettings",
        "primary_field": "button_text",
        "sections": [],
    },
    {
        "key": "home",
        "title": "Home Management",
        "icon": "fas fa-home",
        "description": "Sections that build the public homepage.",
        "index_url": "dashboard:home_module",
        "sections": [
            {
                "key": "hero",
                "title": "Hero Section",
                "icon": "fas fa-bullhorn",
                "url_name": "dashboard:hero_edit",
                "description": "Top banner: headline, description, CTAs, background.",
                "loader": "home.models.HeroSection",
                "primary_field": "title",
            },
            {
                "key": "feature",
                "title": "Feature Section",
                "icon": "fas fa-th-large",
                "url_name": "dashboard:feature_edit",
                "description": "Five highlight cards shown below the hero.",
                "loader": "home.models.FeatureSection",
                "primary_field": "features_title",
            },
            {
                "key": "about",
                "title": "Mission Section",
                "icon": "fas fa-bullseye",
                "url_name": "dashboard:about_edit",
                "description": "About / mission statement block.",
                "loader": "home.models.AboutSection",
                "primary_field": "about_section_title",
            },
            {
                "key": "network",
                "title": "Network Section",
                "icon": "fas fa-network-wired",
                "url_name": "dashboard:network_edit",
                "description": "Network stats block — heading, optional video, plus selectable statistics from Data Management.",
                "loader": "home.models.NetworkSection",
                "primary_field": "network_section_title",
            },
            {
                "key": "talent_pool",
                "title": "Talent Pool Section",
                "icon": "fas fa-users",
                "url_name": "dashboard:talent_pool_edit",
                "description": "Talent Pool block — label, title, subtitle, description, CTAs, image.",
                "loader": "home.models.TalentPoolSection",
                "primary_field": "talent_pool_section_title",
            },
            {
                "key": "apply",
                "title": "Apply Section",
                "icon": "fas fa-paper-plane",
                "url_name": "dashboard:apply_edit",
                "description": "Apply block — heading, sub-heading and 3 fixed company cards.",
                "loader": "home.models.ApplySection",
                "primary_field": "apply_section_title",
            },
            {
                "key": "social_media",
                "title": "Social Media Section",
                "icon": "fas fa-share-alt",
                "url_name": "dashboard:social_media_edit",
                "description": "Social Media block — heading and a manual list of social cards.",
                "loader": "home.models.SocialMediaSection",
                "primary_field": "heading",
            },
            {
                "key": "testimonials",
                "title": "Testimonials Section",
                "icon": "fas fa-quote-right",
                "url_name": "dashboard:testimonials_edit",
                "description": "Testimonials block — title, background images, and per-section messages from picked team members.",
                "loader": "home.models.TestimonialsSection",
                "primary_field": "title",
            },
            {
                "key": "app",
                "title": "App Section",
                "icon": "fas fa-mobile-alt",
                "url_name": "dashboard:app_edit",
                "description": "App promotion — title, description, 3 buttons, side image, barcode.",
                "loader": "home.models.AppSection",
                "primary_field": "title",
            },
        ],
    },
    {
        "key": "about_us",
        "title": "About Management",
        "icon": "fas fa-id-card",
        "description": "Sections that build the public About Us page.",
        "index_url": "dashboard:about_us_module",
        "sections": [
            {
                "key": "hero",
                "title": "Hero Section",
                "icon": "fas fa-bullhorn",
                "url_name": "dashboard:about_us_hero_edit",
                "description": "Top banner: label, title, description, background image.",
                "loader": "about_us.models.AboutUsHeroSection",
                "primary_field": "title",
            },
            {
                "key": "mission",
                "title": "Mission Section",
                "icon": "fas fa-bullseye",
                "url_name": "dashboard:about_us_mission_edit",
                "description": "Mission block — label, title, description, statistics.",
                "loader": "about_us.models.AboutUsMissionSection",
                "primary_field": "title",
            },
            {
                "key": "founder",
                "title": "Founder Section",
                "icon": "fas fa-user-tie",
                "url_name": "dashboard:about_us_founder_edit",
                "description": "Founder block — name, designation, description, message, button, side image.",
                "loader": "about_us.models.AboutUsFounderSection",
                "primary_field": "founder_name",
            },
            {
                "key": "values",
                "title": "Values Section",
                "icon": "fas fa-heart",
                "url_name": "dashboard:about_us_values_edit",
                "description": "Values block — label, title, sub-title, plus a manual list of value cards.",
                "loader": "about_us.models.AboutUsValuesSection",
                "primary_field": "title",
            },
            {
                "key": "journey",
                "title": "Journey Section",
                "icon": "fas fa-route",
                "url_name": "dashboard:about_us_journey_edit",
                "description": "Journey block — label, title, sub-title, plus a manual list of journey cards.",
                "loader": "about_us.models.AboutUsJourneySection",
                "primary_field": "title",
            },
            {
                "key": "pledge",
                "title": "Pledge Section",
                "icon": "fas fa-handshake",
                "url_name": "dashboard:about_us_pledge_edit",
                "description": "Pledge block — label, title, description, side image.",
                "loader": "about_us.models.AboutUsPledgeSection",
                "primary_field": "title",
            },
            {
                "key": "team",
                "title": "Team Section",
                "icon": "fas fa-user-friends",
                "url_name": "dashboard:about_us_team_edit",
                "description": "Team block — label, title, sub-title, plus a manual list of member cards.",
                "loader": "about_us.models.AboutUsTeamSection",
                "primary_field": "title",
            },
            {
                "key": "community",
                "title": "Community Section",
                "icon": "fas fa-people-carry",
                "url_name": "dashboard:about_us_community_edit",
                "description": "Community block — label, title, sub-title, plus a manual list of community cards.",
                "loader": "about_us.models.AboutUsCommunitySection",
                "primary_field": "title",
            },
            {
                "key": "social_media",
                "title": "Social Media Section",
                "icon": "fas fa-share-alt",
                "url_name": "dashboard:about_us_social_media_edit",
                "description": "Social Media block — independent label/title/sub-title; cards are shared with Home → Social Media.",
                "loader": "about_us.models.AboutUsSocialMediaSection",
                "primary_field": "heading",
            },
        ],
    },
    {
        "key": "schools",
        "title": "Schools Management",
        "icon": "fas fa-school",
        "description": "Sections that build the public Schools page.",
        "index_url": "dashboard:schools_module",
        "sections": [
            {
                "key": "hero",
                "title": "Hero Section",
                "icon": "fas fa-bullhorn",
                "url_name": "dashboard:schools_hero_edit",
                "description": "Top banner: label, title, description, two CTAs, side image.",
                "loader": "schools.models.SchoolsHeroSection",
                "primary_field": "title",
            },
            {
                "key": "help",
                "title": "Help Section",
                "icon": "fas fa-question-circle",
                "url_name": "dashboard:schools_help_edit",
                "description": "Help block — label, title, plus a manual list of help cards.",
                "loader": "schools.models.SchoolsHelpSection",
                "primary_field": "title",
            },
            {
                "key": "employer",
                "title": "Employer Section",
                "icon": "fas fa-briefcase",
                "url_name": "dashboard:schools_employer_edit",
                "description": "Employer block — label, title, description, CTA, plus selectable employers from Data Management.",
                "loader": "schools.models.SchoolsEmployerSection",
                "primary_field": "title",
            },
            {
                "key": "benchmark",
                "title": "Benchmark Section",
                "icon": "fas fa-chart-line",
                "url_name": "dashboard:schools_benchmark_edit",
                "description": "Benchmark block — label, title, description, plus a manual list of benchmark cards.",
                "loader": "schools.models.SchoolsBenchmarkSection",
                "primary_field": "title",
            },
            {
                "key": "subscribe",
                "title": "Subscribe Section",
                "icon": "fas fa-envelope-open-text",
                "url_name": "dashboard:schools_subscribe_edit",
                "description": "Subscribe block — label, title, description, CTA, side image, plus a manual list of form fields.",
                "loader": "schools.models.SchoolsSubscribeSection",
                "primary_field": "title",
            },
            {
                "key": "faq",
                "title": "FAQ Section",
                "icon": "fas fa-question",
                "url_name": "dashboard:schools_faq_edit",
                "description": "FAQ block — label, title, description, plus a manual list of Q&A items.",
                "loader": "schools.models.SchoolsFaqSection",
                "primary_field": "title",
            },
        ],
    },
    {
        "key": "employers",
        "title": "Employers Management",
        "icon": "fas fa-briefcase",
        "description": "Sections that build the public Employers page.",
        "index_url": "dashboard:employers_module",
        "sections": [
            {
                "key": "hero",
                "title": "Hero Section",
                "icon": "fas fa-bullhorn",
                "url_name": "dashboard:employers_hero_edit",
                "description": "Top banner: label, title, description, two CTAs, side image.",
                "loader": "employers.models.EmployersHeroSection",
                "primary_field": "title",
            },
            {
                "key": "network",
                "title": "Network Section",
                "icon": "fas fa-chart-bar",
                "url_name": "dashboard:employers_network_edit",
                "description": "Network stats — shares the home Network singleton and its selection of statistics.",
                "loader": "home.models.NetworkSection",
                "primary_field": "network_section_title",
            },
            {
                "key": "mission",
                "title": "Mission Section",
                "icon": "fas fa-bullseye",
                "url_name": "dashboard:employers_mission_edit",
                "description": "Mission block — label, title, description, plus a manual list of bullet points.",
                "loader": "employers.models.EmployersMissionSection",
                "primary_field": "title",
            },
            {
                "key": "offer",
                "title": "Offers Section",
                "icon": "fas fa-gift",
                "url_name": "dashboard:employers_offer_edit",
                "description": "Offers block — label, title, description, plus a manual list of offer cards.",
                "loader": "employers.models.EmployersOfferSection",
                "primary_field": "title",
            },
            {
                "key": "events",
                "title": "Events Section",
                "icon": "fas fa-calendar-alt",
                "url_name": "dashboard:employers_events_edit",
                "description": "Events block — label, title, description, CTA, plus a manual list of event images.",
                "loader": "employers.models.EmployersEventsSection",
                "primary_field": "title",
            },
        ],
    },
    {
        "key": "partners",
        "title": "Partner Management",
        "icon": "fas fa-handshake",
        "description": "Sections that build the public Partners page.",
        "index_url": "dashboard:partners_module",
        "sections": [
            {
                "key": "hero",
                "title": "Hero Section",
                "icon": "fas fa-bullhorn",
                "url_name": "dashboard:partners_hero_edit",
                "description": "Top banner: label, title, description, plus selectable statistics from Data Management.",
                "loader": "partners.models.PartnersHeroSection",
                "primary_field": "title",
            },
            {
                "key": "partner_section",
                "title": "Partner Section",
                "icon": "fas fa-th-list",
                "url_name": "dashboard:partners_partner_section_edit",
                "description": "Search placeholder + a manual list of partner categories.",
                "loader": "partners.models.PartnersPartnerSection",
                "primary_field": "search_placeholder",
            },
            {
                "key": "family_section",
                "title": "Family Section",
                "icon": "fas fa-users",
                "url_name": "dashboard:partners_family_section_edit",
                "description": "Label, title, description, selectable employers, and a Load More CTA.",
                "loader": "partners.models.PartnersFamilySection",
                "primary_field": "title",
            },
            {
                "key": "review_section",
                "title": "Review Section",
                "icon": "fas fa-quote-right",
                "url_name": "dashboard:partners_review_section_edit",
                "description": "Label, title, plus a manual list of review cards (name, designation, message).",
                "loader": "partners.models.PartnersReviewSection",
                "primary_field": "title",
            },
            {
                "key": "founder_section",
                "title": "Founder Section",
                "icon": "fas fa-user-tie",
                "url_name": "dashboard:partners_founder_section_edit",
                "description": "Label, title, description, plus two CTA buttons.",
                "loader": "partners.models.PartnersFounderSection",
                "primary_field": "title",
            },
        ],
    },
    {
        "key": "events",
        "title": "Events Management",
        "icon": "fas fa-calendar-alt",
        "description": "Sections that build the public Events page.",
        "index_url": "dashboard:events_module",
        "sections": [
            {
                "key": "hero",
                "title": "Hero Section",
                "icon": "fas fa-bullhorn",
                "url_name": "dashboard:events_hero_edit",
                "description": "Top banner: label, title, description, and two CTA buttons.",
                "loader": "events.models.EventsHeroSection",
                "primary_field": "title",
            },
            {
                "key": "featured",
                "title": "Featured Section",
                "icon": "fas fa-star",
                "url_name": "dashboard:events_featured_edit",
                "description": "Label, date/time line, title, description, category label, and a CTA button.",
                "loader": "events.models.EventsFeaturedSection",
                "primary_field": "title",
            },
            {
                "key": "upcoming",
                "title": "Upcoming Events",
                "icon": "fas fa-calendar-plus",
                "url_name": "dashboard:events_upcoming_edit",
                "description": "Label, title, plus manual lists of category labels and event cards.",
                "loader": "events.models.EventsUpcomingSection",
                "primary_field": "title",
            },
            {
                "key": "missed",
                "title": "Missed Events",
                "icon": "fas fa-video",
                "url_name": "dashboard:events_missed_edit",
                "description": "Label, title, description, plus a manual list of missed event cards (video, title, date, button URL).",
                "loader": "events.models.EventsMissedSection",
                "primary_field": "title",
            },
            {
                "key": "submit",
                "title": "Submit Events",
                "icon": "fas fa-paper-plane",
                "url_name": "dashboard:events_submit_edit",
                "description": "Label, title, description, single CTA button, plus a side image.",
                "loader": "events.models.EventsSubmitSection",
                "primary_field": "title",
            },
        ],
    },
    {
        "key": "insight",
        "title": "Insight Management",
        "icon": "fas fa-lightbulb",
        "description": "Sections that build the public Insight page.",
        "index_url": "dashboard:insight_module",
        "sections": [
            {
                "key": "hero",
                "title": "Hero Section",
                "icon": "fas fa-bullhorn",
                "url_name": "dashboard:insight_hero_edit",
                "description": "Top banner: label, title, description, search placeholder.",
                "loader": "insight.models.InsightHeroSection",
                "primary_field": "title",
            },
            {
                "key": "founder_section",
                "title": "Founder Section",
                "icon": "fas fa-user-tie",
                "url_name": "dashboard:insight_founder_section_edit",
                "description": "Category labels, label-1/label-2, date, title, description, meta line, CTA, images.",
                "loader": "insight.models.InsightFounderSection",
                "primary_field": "title",
            },
            {
                "key": "article_section",
                "title": "Article Section",
                "icon": "fas fa-newspaper",
                "url_name": "dashboard:insight_article_section_edit",
                "description": "Title + shared card button text, plus a manual list of article cards.",
                "loader": "insight.models.InsightArticleSection",
                "primary_field": "title",
            },
            {
                "key": "lane_section",
                "title": "Lane Section",
                "icon": "fas fa-road",
                "url_name": "dashboard:insight_lane_section_edit",
                "description": "Label + title, plus a manual list of lanes (name, article count, URL).",
                "loader": "insight.models.InsightLaneSection",
                "primary_field": "title",
            },
            {
                "key": "subscribe_section",
                "title": "Subscribe Section",
                "icon": "fas fa-envelope-open-text",
                "url_name": "dashboard:insight_subscribe_section_edit",
                "description": "Label, title, description, email input, subscribe CTA, bottom note, images.",
                "loader": "insight.models.InsightSubscribeSection",
                "primary_field": "title",
            },
        ],
    },
    {
        "key": "data",
        "title": "Data Management",
        "icon": "fas fa-database",
        "description": "Shared dynamic data (Statistics, Employers) reused across pages.",
        "index_url": "dashboard:data_module",
        "sections": [
            {
                "key": "team_members",
                "title": "Team Members",
                "icon": "fas fa-user-friends",
                "url_name": "dashboard:team_members_edit",
                "description": "Add, edit and remove team members that the About Us Team section can select from.",
                "loader": None,
                "primary_field": None,
            },
            {
                "key": "employers",
                "title": "Employers",
                "icon": "fas fa-briefcase",
                "url_name": "dashboard:employers_edit",
                "description": "Add, edit and remove employer logos that the Schools Employer section can select from.",
                "loader": None,
                "primary_field": None,
            },
            {
                "key": "social_media",
                "title": "Social Media",
                "icon": "fas fa-share-alt",
                "url_name": "dashboard:social_media_icons_edit",
                "description": "Add, edit and remove social media icons that the Home and About Us social media sections can select from.",
                "loader": None,
                "primary_field": None,
            },
            {
                "key": "statistics",
                "title": "Statistics",
                "icon": "fas fa-chart-bar",
                "url_name": "dashboard:statistics_edit",
                "description": "Add, edit and remove statistics that the Network, Mission and Partners Hero sections can select from.",
                "loader": None,
                "primary_field": None,
            },
        ],
    },
    {
        "key": "footer",
        "title": "Footer Management",
        "icon": "fas fa-shoe-prints",
        "description": "Site-wide footer — logo, contact details, copyright, and links.",
        "flat": True,
        "index_url": "dashboard:footer_edit",
        "loader": "home.models.FooterSettings",
        "primary_field": "title",
        "sections": [],
    },
]


def _import_loader(path: str):
    module_path, _, attr = path.rpartition(".")
    from importlib import import_module

    return getattr(import_module(module_path), attr)


def get_module(key: str) -> dict | None:
    for module in DASHBOARD_MODULES:
        if module["key"] == key:
            return module
    return None


def section_url_names(module: dict) -> list[str]:
    """Url names (without the namespace) for a module's sections — used for
    the sidebar's active/menu-open state."""
    names = []
    for section in module["sections"]:
        _, _, name = section["url_name"].partition(":")
        names.append(name)
    return names


def _section_is_configured(section: dict) -> bool:
    loader_path = section.get("loader")
    field = section.get("primary_field")
    if not loader_path or not field:
        return False
    try:
        instance = _import_loader(loader_path).load()
    except Exception:
        return False
    return bool(getattr(instance, field, None))


def module_stats(module: dict) -> dict:
    """Return {total, configured, sections} for a module — each section in
    `sections` is annotated with `is_configured`. Flat modules (no nested
    sections) report total/configured against their own loader."""
    if module.get("flat"):
        configured = 1 if _section_is_configured(module) else 0
        return {"total": 1, "configured": configured, "sections": []}

    sections = []
    configured = 0
    for section in module["sections"]:
        is_configured = _section_is_configured(section)
        if is_configured:
            configured += 1
        sections.append({**section, "is_configured": is_configured})
    return {
        "total": len(module["sections"]),
        "configured": configured,
        "sections": sections,
    }
