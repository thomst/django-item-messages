from django.conf import settings
from django.utils.module_loading import import_string


def default_storage(request):
    """
    Callable with the same interface as the storage classes.

    This isn't just default_storage =
    import_string(settings.ITEM_MESSAGE_STORAGE) to avoid accessing the settings
    at the module level.
    """
    default = 'item_messages.storage.session.SessionStorage'
    return import_string(getattr(settings, 'ITEM_MESSAGE_STORAGE', default))(request)