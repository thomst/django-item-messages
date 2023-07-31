from django.contrib.messages.storage.session import SessionStorage as BaseSessionStorage
from .base import StorageMixin


class SessionStorage(StorageMixin, BaseSessionStorage):
    """
    Store messages in the session (that is, django.contrib.sessions).
    """
    session_key = "_item_messages"
