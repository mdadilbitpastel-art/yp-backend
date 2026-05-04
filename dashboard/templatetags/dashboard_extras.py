"""Template helpers used by the home-management form."""

from django import template

register = template.Library()


@register.filter(name="get_field")
def get_field(form, name):
    """Return a bound form field by name — used to render specific fields
    inside grouped section cards."""
    try:
        return form[name]
    except KeyError:
        return ""
