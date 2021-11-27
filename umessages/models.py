

from django.db import models
from django.contrib.auth.models import User
from .managers import (
    MessageManager,
    MessageContactManager,
    MessageRecipientManager,
)


class MessageContact(models.Model):
    um_from_user = models.ForeignKey(
        User,
        verbose_name=("from user"),
        related_name=("um_from_users"),
        on_delete=models.CASCADE,
    )
    um_to_user = models.ForeignKey(
        User,
        verbose_name=("to user"),
        related_name=("um_to_users"),
        on_delete=models.CASCADE,
    )
    latest_message = models.ForeignKey(
        "Message", verbose_name=("latest message"), on_delete=models.CASCADE
    )
    objects = MessageContactManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["um_from_user", "um_to_user"], name="latestmessage"
            )
        ]
        verbose_name = "contact"
        verbose_name_plural = "contacts"

    def __str__(self):
        return ("%(um_from_user)s and %(um_to_user)s") % {
            "um_from_user": self.um_from_user.username,
            "um_to_user": self.um_to_user.username,
        }

    def opposite_user(self, user):
        if self.um_from_user == user:
            return self.um_to_user
        return self.um_from_user


class MessageRecipient(models.Model):
    user = models.ForeignKey(
        User, verbose_name=("recipient"), on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        "Message", verbose_name=("message"), on_delete=models.CASCADE
    )
    read_at = models.DateTimeField(("read at"), null=True, blank=True)
    deleted_at = models.DateTimeField(("recipient deleted at"), null=True, blank=True)

    objects = MessageRecipientManager()

    class Meta:
        verbose_name = ("recipient")
        verbose_name_plural = ("recipients")

    def __str__(self):
        return ("%(message)s") % {"message": self.message}

    def is_read(self):
        return self.read_at is None


class Message(models.Model):
    body = models.TextField(("body"))
    sender = models.ForeignKey(
        User,
        related_name="sent_messages",
        verbose_name=("sender"),
        on_delete=models.CASCADE,
    )
    recipients = models.ManyToManyField(
        User,
        through="MessageRecipient",
        related_name="received_messages",
        verbose_name=("recipients"),
    )
    sent_at = models.DateTimeField(("sent at"), auto_now_add=True)
    sender_deleted_at = models.DateTimeField(
        ("sender deleted at"), null=True, blank=True
    )
    objects = MessageManager()

    class Meta:
        ordering = ["-sent_at"]
        verbose_name = ("message")
        verbose_name_plural = ("messages")

    def save_recipients(self, um_to_user_list):
        created = False
        for user in um_to_user_list:
            MessageRecipient.objects.create(user=user, message=self)
            created = True
        return created

    def update_contacts(self, um_to_user_list):
        updated = False
        for user in um_to_user_list:
            MessageContact.objects.update_contact(self.sender, user, self)
            updated = True
        return updated
