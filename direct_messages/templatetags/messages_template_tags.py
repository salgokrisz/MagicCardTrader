from django import template
from direct_messages.models import Message

register = template.Library()

@register.filter

def unread_message_counter(user):
    if user.is_authenticated:
        total_unread = 0
        messages = Message.get_messages(user=user)
        for message in messages:
            total_unread = total_unread + message['unread']
        return total_unread