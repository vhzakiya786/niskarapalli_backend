from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    # breakpoint()
    return getattr(obj, attr_name, None)
