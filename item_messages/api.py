from django.contrib.messages import constants
from django.contrib.messages.api import MessageFailure
from .storage import default_storage

__all__ = (
    "add_message",
    "clear_messages",
    "get_messages",
    "get_level",
    "set_level",
    "debug",
    "info",
    "success",
    "warning",
    "error",
    "MessageFailure",
)


def add_message(request, level, obj, message, extra_tags=""):
    """
    Attempt to add a message to the request using the 'messages' app.
    """
    try:
        messages = request._item_messages
    except AttributeError as exc:
        raise MessageFailure(
            "You cannot add messages without installing "
            "django.contrib.messages.middleware.MessageMiddleware"
        ) from exc
    else:
        return messages.add(level, obj, message, extra_tags)


def clear_messages(request, obj):
    """
    TODO
    """
    try:
        messages = request._item_messages
    except AttributeError as exc:
        raise MessageFailure(
            "You cannot add messages without installing "
            "django.contrib.messages.middleware.MessageMiddleware"
        ) from exc
    else:
        return messages.clear(obj)


def get_messages(request):
    """
    Return the message storage on the request if it exists, otherwise return
    an empty list.
    """
    return getattr(request, "_item_messages", dict())


def get_level(request):
    """
    Return the minimum level of messages to be recorded.

    The default level is the ``MESSAGE_LEVEL`` setting. If this is not found,
    use the ``INFO`` level.
    """
    storage = getattr(request, "_item_messages", default_storage(request))
    return storage.level


def set_level(request, level):
    """
    Set the minimum level of messages to be recorded, and return ``True`` if
    the level was recorded successfully.

    If set to ``None``, use the default level (see the get_level() function).
    """
    if not hasattr(request, "_item_messages"):
        return False
    request._item_messages.level = level
    return True


def debug(request, obj, message, extra_tags=""):
    """Add a message with the ``DEBUG`` level."""
    add_message(
        request,
        constants.DEBUG,
        obj,
        message,
        extra_tags=extra_tags,
    )


def info(request, obj, message, extra_tags=""):
    """Add a message with the ``INFO`` level."""
    add_message(
        request,
        constants.INFO,
        obj,
        message,
        extra_tags=extra_tags,
    )


def success(request, obj, message, extra_tags=""):
    """Add a message with the ``SUCCESS`` level."""
    add_message(
        request,
        constants.SUCCESS,
        obj,
        message,
        extra_tags=extra_tags,
    )


def warning(request, obj, message, extra_tags=""):
    """Add a message with the ``WARNING`` level."""
    add_message(
        request,
        constants.WARNING,
        obj,
        message,
        extra_tags=extra_tags,
    )


def error(request, obj, message, extra_tags=""):
    """Add a message with the ``ERROR`` level."""
    add_message(
        request,
        constants.ERROR,
        obj,
        message,
        extra_tags=extra_tags,
    )

def clear(request, obj):
    """Clear all messages of a given object."""
    clear_messages(request, obj)