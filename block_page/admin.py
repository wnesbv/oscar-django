from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


from block_page.models import SlidesFlatPage, SlidesFlatShow, ShowSlideBlock, ShowSlide


class SlidesFlatPageInline(GenericTabularInline):
    model = SlidesFlatPage

class SlidesFlatShowAdmin(admin.ModelAdmin):
    list_display = ("slides_show_name", "published")
    inlines = [SlidesFlatPageInline]


# ...
class ShowSlideBlockInline(GenericTabularInline):
    model = ShowSlideBlock

class ShowSlideAdmin(admin.ModelAdmin):
    list_display = ("slides_show_name", "published")
    inlines = [ShowSlideBlockInline]


admin.site.register(SlidesFlatShow, SlidesFlatShowAdmin)
admin.site.register(ShowSlide, ShowSlideAdmin)
