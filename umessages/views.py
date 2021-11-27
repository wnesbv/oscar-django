
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic import (
    UpdateView,
    DeleteView,
)
from .forms import ComposeForm
from .models import Message, MessageRecipient, MessageContact
from .utils import get_datetime_now


class MessageListView(ListView):
    page = 1
    paginate_by = 10
    template_name = "umessages/message_list.html"
    extra_context = {}
    context_object_name = "message_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get_queryset(self):
        return MessageContact.objects.get_contacts_for(self.request.user)

class MessageDetailListView(MessageListView):
    template_name = "umessages/message_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipient"] = self.recipient
        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        self.recipient = get_object_or_404(get_user_model(), username__iexact=username)
        queryset = Message.objects.get_conversation_between(
            self.request.user, self.recipient
        )
        self._update_unread_messages(queryset)
        return queryset

    def _update_unread_messages(self, queryset):
        message_pks = [m.pk for m in queryset]
        unread_list = MessageRecipient.objects.filter(
            message__in=message_pks, user=self.request.user, read_at__isnull=True
        )
        now = get_datetime_now()
        unread_list.update(read_at=now)


@login_required
def message_compose(
    request,
    recipients=None,
    compose_form=ComposeForm,
    success_url=None,
    template_name="umessages/message_form.html",
    extra_context=None,
):
    extra_context = []
    master = User.objects.all()

    initial_data = dict()
    if recipients:
        username_list = [r.strip() for r in recipients.split("+")]
        recipients = [
            tuple(map(float, u))
            for u in get_user_model().objects.filter(username__in=username_list)
        ]
        initial_data["to"] = recipients
    form = compose_form(initial=initial_data)
    if request.method == "POST":
        form = compose_form(request.POST)
        if form.is_valid():
            requested_redirect = request.GET.get(
                REDIRECT_FIELD_NAME, request.POST.get(REDIRECT_FIELD_NAME, False)
            )
            message = form.save(request.user)
            recipients = form.cleaned_data["to"]
            if message:
                messages.success(request, ("Message is sent."), fail_silently=True)
            redirect_to = reverse("umessages_list")
            if requested_redirect:
                redirect_to = requested_redirect
            elif success_url:
                redirect_to = success_url
            elif len(recipients) == 1:
                redirect_to = reverse(
                    "umessages_detail",
                    kwargs={"username": recipients[0].username},
                )
            return redirect(redirect_to)
    if not extra_context:
        extra_context = dict()
    extra_context["form"] = form
    extra_context["master"] = master
    extra_context["recipients"] = recipients
    return render(request, template_name, extra_context)


class MessageUpdateView(UpdateView):
    model = Message
    fields = [
        "body",
    ]
    template_name = "umessages/message_update_form.html"
    success_url = "/home/messages/"

class MessageDeleteView(DeleteView):
    model = Message
    template_name = "umessages/message_confirm_delete.html"
    success_url = "/home/messages/"
