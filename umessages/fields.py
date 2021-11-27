

from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets


class CommaSeparatedUserInput(widgets.Input):
    input_type = "text"
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ""
        elif isinstance(value, (list, tuple)):
            value = ", ".join([user.username for user in value])
        return super().render(name, value, attrs, renderer)

class CommaSeparatedUserField(forms.Field):
    widget = CommaSeparatedUserInput
    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop("recipient_filter", None)
        self._recipient_filter = recipient_filter
        super().__init__(*args, **kwargs)

    def clean(self, value):
        super().clean(value)
        names = set(value.split(","))
        names_set = set([name.strip() for name in names])
        users = list(get_user_model().objects.filter(username__in=names_set))

        # Check for unknown names.
        unknown_names = names_set ^ set([user.username for user in users])
        recipient_filter = self._recipient_filter
        invalid_users = []
        if recipient_filter is not None:
            for r in users:
                if recipient_filter(r) is False:
                    users.remove(r)
                    invalid_users.append(r.username)
        if unknown_names or invalid_users:
            humanized_usernames = ", ".join(list(unknown_names) + invalid_users)
            raise forms.ValidationError(
                ("The following usernames are incorrect: %(users)s.")
                % {"users": humanized_usernames}
            )
        return users
