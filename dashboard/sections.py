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
                "icon": "fas fa-chart-bar",
                "url_name": "dashboard:network_edit",
                "description": "Network stats block — heading, optional video, 4 fixed stats.",
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
                "description": "Testimonials block — background image and 3 fixed user cards.",
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
