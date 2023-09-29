from django.contrib.messages.storage.base import Message as BaseMessage
from ..utils import get_msg_path
from ..utils import get_msg_id
from ..utils import get_model_id


class Message(BaseMessage):
    def __init__(self, obj, level, message, extra_tags=None, extra_data=None):
        super().__init__(level, message, extra_tags)
        self.model_id, self.obj_id = get_msg_path(obj)
        self.extra_data = extra_data or {}

    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return (
            self.level == other.level
            and self.message == other.message
            and self.obj_id == other.obj_id
            and self.model_id == other.model_id
        )


# FIXME: Make this class a dict type.
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
    def _messages(self):
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
        self._prepare_messages(self._messages)
        return self._store(self._messages, response)

    def add(self, obj, level, message, extra_tags="", extra_data=None):
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
        msg = Message(obj, level, message, extra_tags, extra_data)

        # Prepare the queued_messages dictonary.
        if not msg.model_id in self._messages:
            self._messages[msg.model_id] = dict()
        if not msg.obj_id in self._messages[msg.model_id]:
            self._messages[msg.model_id][msg.obj_id] = list()

        # Add message.
        obj_msgs = self._messages[msg.model_id][msg.obj_id]
        index = len(obj_msgs)
        obj_msgs.append(msg)
        return get_msg_id(msg, index)

    def update_message(self, msg_id, message, level=None, extra_tags="", extra_data=None):
        """
        _summary_

        :param str msg_id: _description_
        :param str message: _description_
        """
        model_id, obj_id, index = msg_id.split(':')
        try:
            original_msg = self._messages.get(model_id, dict()).get(obj_id, list())[index]
        except IndexError:
            pass
        else:
            msg = Message(
                level or original_msg.level,
                original_msg.obj,
                message,
                extra_tags or original_msg.extra_tags,
                extra_data or original_msg.extra_data,
                )
            self._messages[model_id][obj_id][index] = msg

    def get(self, model=None, obj=None, msg_id=None):
        """
        Get either all or model specific or object specific messages.
        """
        if msg_id:
            model_id, obj_id, index = msg_id.split(':')
            try:
                return self._messages.get(model_id, {}).get(obj_id, [])[index]
            except IndexError:
                return None
        elif obj:
            model_id, obj_id = get_msg_path(obj)
            return self._messages.get(model_id, {}).get(obj_id, [])
        elif model:
            return self._messages.get(get_model_id(model), {})
        else:
            return self._messages

    def remove(self, model=None, obj=None, msg_id=None):
        """
        _summary_
        """
        if msg_id:
            model_id, obj_id, index = msg_id.split(':')
            try:
                del self._messages.get(model_id, {}).get(obj_id, [])[index]
            except IndexError:
                pass
        elif obj:
            model_id, obj_id = get_msg_path(obj)
            try:
                del self._messages.get(model_id, {})[obj_id]
            except KeyError:
                pass
        elif model:
            try:
                del self._messages[get_model_id(model)]
            except KeyError:
                pass
        else:
            del self._loaded_data
