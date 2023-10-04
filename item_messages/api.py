from django.contrib.messages.api import MessageFailure
from .storage import default_storage
from . import constants


__all__ = (
    "add_message",
    "update_message",
    "remove_messages",
    "get_messages",
    "get_level",
    "set_level",
    "debug",
    "item_debug",
    "info",
    "item_info",
    "success",
    "item_success",
    "warning",
    "item_warning",
    "error",
    "item_error",
    "MessageFailure",
)


def _get_storage(request):
    try:
        return request._item_messages
    except AttributeError as exc:
        raise MessageFailure(
            "You cannot use item messages without installing ``item_messages``."
        ) from exc


def add_message(request, obj, level, message, extra_tags="", extra_data=None):
    """
    Attempt to add a message to the request using the 'messages' app.
    """
    messages = _get_storage(request)
    return messages.add(obj, level, message, extra_tags, extra_data)


def update_message(request, msg_id, level=None, message="", extra_tags="", extra_data=None):
    """
    Attempt to update a message to the request using the 'messages' app.
    """
    messages = _get_storage(request)
    return messages.update_message(msg_id, level, message, extra_tags, extra_data)


def remove_messages(request, model=None, obj=None, msg_id=None):
    """
    _summary_

    :param _type_ request: _description_
    :param _type_ model: _description_, defaults to None
    :param _type_ obj: _description_, defaults to None
    :param _type_ msg_id: _description_, defaults to None
    :return _type_: _description_
    """
    messages = _get_storage(request)
    return messages.remove(model, obj, msg_id)


def get_messages(request, model=None, obj=None, msg_id=None):
    """
    _summary_

    :param _type_ request: _description_
    :param _type_ model: _description_, defaults to None
    :param _type_ obj: _description_, defaults to None
    :param _type_ msg_id: _description_, defaults to None
    :return _type_: _description_
    """
    messages = _get_storage(request)
    return messages.get(model, obj, msg_id)


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
    add_message(request, obj, constants.DEBUG, message, extra_tags=extra_tags)

#: Synonym for :func:`~.debug`.
item_debug = debug

def info(request, obj, message, extra_tags=""):
    """Add a message with the ``INFO`` level."""
    add_message(request, obj, constants.INFO, message, extra_tags=extra_tags)

#: Synonym for :func:`~.info`.
item_info = info


def success(request, obj, message, extra_tags=""):
    """Add a message with the ``SUCCESS`` level."""
    add_message(request, obj, constants.SUCCESS, message, extra_tags=extra_tags)

#: Synonym for :func:`~.success`.
item_success = success


def warning(request, obj, message, extra_tags=""):
    """Add a message with the ``WARNING`` level."""
    add_message(request, obj, constants.WARNING, message, extra_tags=extra_tags)

#: Synonym for :func:`~.warning`.
item_warning = warning


def error(request, obj, message, extra_tags=""):
    """Add a message with the ``ERROR`` level."""
    add_message(request, obj, constants.ERROR, message, extra_tags=extra_tags)

#: Synonym for :func:`~.error`.
item_error = error
