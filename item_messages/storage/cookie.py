from django.contrib.messages.storage.cookie import CookieStorage as BaseCookieStorage
from .base import StorageMixin


class CookieStorage(StorageMixin, BaseCookieStorage):
    """
    Store messages in a cookie.
    """

    cookie_name = "item_messages"
    key_salt = "django-item-messages"
