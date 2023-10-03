from django.contrib.messages.constants import DEFAULT_LEVELS
from .api import get_messages


def item_messages(request):
    """
    Return a lazy 'messages' context variable as well as
    'DEFAULT_MESSAGE_LEVELS'.
    """
    return {
        "item_messages": getattr(request, '_item_messages', None),
        "DEFAULT_MESSAGE_LEVELS": DEFAULT_LEVELS,
    }
