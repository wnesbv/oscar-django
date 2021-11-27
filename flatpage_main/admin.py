
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = FlatPage
        fields = "__all__"

class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
