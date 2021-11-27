

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from block_page.models import SlidesFlatPage, SlidesFlatShow


# ...
class SlidesFlatPageInline(GenericTabularInline):
    model = SlidesFlatPage

class SlidesFlatShowAdmin(admin.ModelAdmin):
    list_display = ("slides_show_name", "published")
    inlines = [SlidesFlatPageInline]


admin.site.register(SlidesFlatShow, SlidesFlatShowAdmin)
