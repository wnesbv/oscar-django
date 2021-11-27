

from django import template
from django.contrib.flatpages.models import FlatPage

register = template.Library()

# ...
@register.inclusion_tag("flatpages/partials/_flatpages_pages.html")
def flatpages_pages():
    flatpages_list = FlatPage.objects.all()
    return {"flatpages_list": flatpages_list}

@register.simple_tag
def total_flatpages():
    return FlatPage.objects.count()
