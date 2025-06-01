# clubs/templatetags/form_tags.py

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css})
    return field  # If not a BoundField, just return it safely
