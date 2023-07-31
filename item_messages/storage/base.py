from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.storage.base import Message as BaseMessage


class Message(BaseMessage):
    def __init__(self, level, obj, message, extra_tags=None):
        super().__init__(level, message, extra_tags)
        self.obj_id = str(obj.id)
        self.content_type_id = str(ContentType.objects.get_for_model(type(obj)).id)

    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return (
            self.level == other.level
            and self.message == other.message
            and self.obj_id == other.obj_id
            and self.content_type_id == other.content_type_id
        )


class StorageMixin:
    def _prepare_messages(self, messages):
        """
        Prepare a list of messages for storage.
        """
        for model_msgs in messages.values():
            for obj_msgs in model_msgs.values():
                for msg in obj_msgs:
                    msg._prepare()

    @property
    def _loaded_messages(self):
        """
        TODO
        """
        if not hasattr(self, "_loaded_data"):
            messages, _ = self._get()
            self._loaded_data = messages or dict()
        return self._loaded_data

    def update(self, response):
        """
        TODO
        """
        self._prepare_messages(self._loaded_messages)
        return self._store(self._loaded_messages, response)

    def add(self, level, obj, message, extra_tags=""):
        """
        TODO
        """
        if not message:
            return

        # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return

        # Add the message.
        msg = Message(level, obj, message, extra_tags=extra_tags)

        # Prepare the queued_messages dictonary.
        if not msg.content_type_id in self._loaded_messages:
            self._loaded_messages[msg.content_type_id] = dict()
        if not msg.obj_id in self._loaded_messages[msg.content_type_id]:
            self._loaded_messages[msg.content_type_id][msg.obj_id] = list()

        self._loaded_messages[msg.content_type_id][msg.obj_id].append(msg)

    def replace(self, level, obj, message, extra_tags=""):
        """
        TODO
        """
        if not message:
            return

        # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return

        # Add the message.
        msg = Message(level, obj, message, extra_tags=extra_tags)

        # Prepare the queued_messages dictonary.
        if not msg.content_type_id in self._loaded_messages:
            self._loaded_messages[msg.content_type_id] = dict()

        self._loaded_messages[msg.content_type_id][msg.obj_id] = list()
        self._loaded_messages[msg.content_type_id][msg.obj_id].append(msg)

    def get(self, model=None, obj=None):
        """
        Get either all or model specific or object specific messages.
        """
        if model:
            content_type_id = ContentType.objects.get_for_model(model).id
            return self._loaded_messages.get(str(content_type_id), dict())
        elif obj:
            content_type_id = ContentType.objects.get_for_model(type(obj)).id
            obj_msgs = self._loaded_messages.get(str(content_type_id), dict())
            return obj_msgs.get(str(obj.id), list())
        else:
            return self._loaded_messages
