from django.contrib.messages.storage.base import Message as BaseMessage


class Message(BaseMessage):
    def __init__(self, level, obj, message, extra_tags=None):
        super().__init__(level, message, extra_tags)
        self.obj_id = str(obj.id)
        self.obj_type_hash = str(hash(type(obj)))

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
        if not msg.obj_type_hash in self._loaded_messages:
            self._loaded_messages[msg.obj_type_hash] = dict()
        if not msg.obj_id in self._loaded_messages[msg.obj_type_hash]:
            self._loaded_messages[msg.obj_type_hash][msg.obj_id] = list()

        self._loaded_messages[msg.content_type_id][msg.obj_id].append(msg)

    def get(self, model=None, obj=None):
        """
        Get either all or model specific or object specific messages.
        """
        if model:
            return self._loaded_messages.get(str(hash(model)), dict())
        elif obj:
            obj_msgs = self._loaded_messages.get(str(hash(type(obj))), dict())
            return obj_msgs.get(str(obj.id), list())
        else:
            return self._loaded_messages

    def clear(self, obj):
        """
        TODO
        """
        obj_type_hash = str(hash(type(obj)))
        obj_id = str(obj.id)

        # Remove all messages for the object and cleanup the loaded_messages
        # dict.
        if obj_type_hash in self._loaded_messages:
            if obj_id in self._loaded_messages[obj_type_hash]:
                del self._loaded_messages[obj_type_hash][obj_id]
            if not self._loaded_messages[obj_type_hash]:
                del self._loaded_messages[obj_type_hash]

    def clear_all(self):
        """
        TODO
        """
        # Remove all messages from loaded_messages.
        del self._loaded_data

