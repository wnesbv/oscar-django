

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from ckeditor.widgets import CKEditorWidget
from oscar.core.loading import get_model
from oscar.core.validators import URLDoesNotExistValidator

FlatPage = get_model('flatpages', 'FlatPage')

class PageSearchForm(forms.Form):
    title = forms.CharField(
        required=False, label=pgettext_lazy("Page title", "Title"))

class PageUpdateForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    url = forms.RegexField(
        label=_("URL"),
        max_length=100,
        regex=r'^[-\w/\.~]+$',
        required=False,
        help_text=_("Example: '/about/contact/'."),
        error_messages={
            "invalid": _(
                "This value must contain only letters, numbers, dots, "
                "underscores, dashes, slashes or tildes."
            ),
        },
    )

    def clean_url(self):
        url = self.cleaned_data['url']
        if 'url' in self.changed_data:
            if not url.endswith('/'):
                url += '/'
            URLDoesNotExistValidator()(url)
        return url

    class Meta:
        model = FlatPage
        fields = ('title', 'url', 'content')
