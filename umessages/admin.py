

from django.contrib.admin import ModelAdmin, TabularInline, site
from .models import Message, MessageContact, MessageRecipient


class MessageRecipientInline(TabularInline):
    model = MessageRecipient

class MessageAdmin(ModelAdmin):
    inlines = [MessageRecipientInline]
    fieldsets = (
        (None, {"fields": ("sender", "body"), "classes": ("monospace")}),
        (
            ("Date/time"),
            {"fields": ("sender_deleted_at",), "classes": ("collapse", "wide")},
        ),
    )
    list_display = ("sender", "id", "body", "sent_at")
    list_filter = ("sent_at", "sender")
    search_fields = ("body",)


site.register(Message, MessageAdmin)
site.register(MessageContact)
