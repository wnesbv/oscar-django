

from django import template
from django.shortcuts import render
from block_page.models import SlidesFlatPage, ShowSlideBlock

register = template.Library()

# ...
@register.inclusion_tag("block_page/partials/_menu_block_page.html")
def menu_block_page():
    slides_list = SlidesFlatPage.objects.all()
    return {"slides_list": slides_list}

@register.inclusion_tag("block_page/slide_block.html")
def slide_block():
    slides_list = SlidesFlatPage.objects.all()
    return {"slides_list": slides_list}

@register.simple_tag
def total_block():
    return SlidesFlatPage.objects.count()

# ...
@register.inclusion_tag("block_page/showslide_block.html")
def showslide_block():
    showslide_list = ShowSlideBlock.objects.all()
    context = {"showslide_list": showslide_list}
    return context
