"""Inject the dashboard module registry into every template so the sidebar
and overview can be rendered without each view having to pass it through."""

from .sections import DASHBOARD_MODULES, section_url_names


def dashboard_nav(request):
    if not request.path.startswith("/dashboard"):
        return {}

    current_url_name = ""
    if getattr(request, "resolver_match", None):
        current_url_name = request.resolver_match.url_name or ""

    modules = []
    for module in DASHBOARD_MODULES:
        child_url_names = section_url_names(module)
        _, _, index_name = module["index_url"].partition(":")
        is_active = (
            current_url_name in child_url_names
            or current_url_name == index_name
        )
        sections_with_bare = []
        for section in module["sections"]:
            _, _, bare = section["url_name"].partition(":")
            sections_with_bare.append({**section, "bare_url_name": bare})
        modules.append(
            {
                **module,
                "sections": sections_with_bare,
                "child_url_names": child_url_names,
                "index_url_name": index_name,
                "is_active": is_active,
                "is_flat": bool(module.get("flat")),
            }
        )

    return {
        "dashboard_modules": modules,
        "current_url_name": current_url_name,
    }
