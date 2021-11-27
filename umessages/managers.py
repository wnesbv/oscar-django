

from django.db import models
from django.db.models import Q
from umessages import signals


class MessageContactManager(models.Manager):
    def get_or_create(self, um_from_user, um_to_user, message):
        created = False
        try:
            contact = self.get(
                Q(um_from_user=um_from_user, um_to_user=um_to_user)
                | Q(um_from_user=um_to_user, um_to_user=um_from_user)
            )
        except self.model.DoesNotExist:
            created = True
            contact = self.create(
                um_from_user=um_from_user, um_to_user=um_to_user, latest_message=message
            )
        return (contact, created)
    def update_contact(self, um_from_user, um_to_user, message):
        contact, created = self.get_or_create(um_from_user, um_to_user, message)
        if not created:
            contact.latest_message = message
            contact.save()
        return contact
    def get_contacts_for(self, user):
        contacts = self.filter(Q(um_from_user=user) | Q(um_to_user=user))
        return contacts


class MessageManager(models.Manager):
    def send_message(self, sender, um_to_user_list, body):
        msg = self.model(sender=sender, body=body)
        msg.save()
        msg.save_recipients(um_to_user_list)
        msg.update_contacts(um_to_user_list)
        signals.email_sent.send(sender=None, msg=msg)
        return msg
    def get_conversation_between(self, um_from_user, um_to_user):
        messages = self.filter(
            Q(
                sender=um_from_user,
                recipients=um_to_user,
                sender_deleted_at__isnull=True,
            )
            | Q(
                sender=um_to_user,
                recipients=um_from_user,
                messagerecipient__deleted_at__isnull=True,
            )
        )
        return messages


class MessageRecipientManager(models.Manager):
    def count_unread_messages_for(self, user):
        unread_total = self.filter(
            user=user, read_at__isnull=True, deleted_at__isnull=True
        ).count()
        return unread_total
    def count_unread_messages_between(self, um_to_user, um_from_user):
        unread_total = self.filter(
            message__sender=um_from_user,
            user=um_to_user,
            read_at__isnull=True,
            deleted_at__isnull=True,
        ).count()
        return unread_total
