

from django import forms
from .models import Message
from .fields import CommaSeparatedUserField


class ComposeForm(forms.Form):
    to = CommaSeparatedUserField(label=("To"))
    body = forms.CharField(
        label=("Message"), widget=forms.Textarea({"class": "message"}), required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["to"].label = "to name:"
        self.fields["body"].label = "message text:"

    def save(self, sender):
        um_to_user_list = self.cleaned_data["to"]
        body = self.cleaned_data["body"]
        msg = Message.objects.send_message(sender, um_to_user_list, body)
        return msg
