from django.contrib.messages.storage.base import Message as BaseMessage


def get_message_id(msg, index):
    """
    _summary_

    :param _type_ msg: _description_
    :param _type_ index: _description_
    :return _type_: _description_
    """
    return f'{msg.obj_type_hash}:{msg.obj_id}:{index}'


class Message(BaseMessage):
    def __init__(self, obj, level, message, extra_tags=None):
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
            and self.obj_type_hash == other.obj_type_hash
        )


class StorageMixin:
    def _prepare_messages(self, messages):
        """
        _summary_
        """
        for model_msgs in messages.values():
            for obj_msgs in model_msgs.values():
                for msg in obj_msgs:
                    msg._prepare()

    @property
    def _loaded_messages(self):
        """
        _summary_
        """
        if not hasattr(self, "_loaded_data"):
            messages, _ = self._get()
            self._loaded_data = messages or dict()
        return self._loaded_data

    def update(self, response):
        """
        _summary_
        """
        self._prepare_messages(self._loaded_messages)
        return self._store(self._loaded_messages, response)

    def add(self, obj, level, message, extra_tags=""):
        """
        _summary_
        """
        if not message:
            return

        # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return

        # Create message object.
        msg = Message(obj, level, message, extra_tags=extra_tags)

        # Prepare the queued_messages dictonary.
        if not msg.obj_type_hash in self._loaded_messages:
            self._loaded_messages[msg.obj_type_hash] = dict()
        if not msg.obj_id in self._loaded_messages[msg.obj_type_hash]:
            self._loaded_messages[msg.obj_type_hash][msg.obj_id] = list()

        # Add message.
        obj_msgs = self._loaded_messages[msg.obj_type_hash][msg.obj_id]
        index = len(obj_msgs)
        obj_msgs.append(msg)
        return get_message_id(msg, index)

    def update_message(self, msg_id, message, level=None, extra_tags=""):
        """
        _summary_

        :param str msg_id: _description_
        :param str message: _description_
        """
        type_hash, obj_id, index = msg_id.split(':')
        try:
            original_msg = self._loaded_messages.get(type_hash, dict()).get(obj_id, list())[index]
        except IndexError:
            pass
        else:
            msg = Message(
                level or original_msg.level,
                original_msg.obj,
                message,
                extra_tags or original_msg.extra_tags)
            self._loaded_messages[type_hash][obj_id][index] = msg

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

