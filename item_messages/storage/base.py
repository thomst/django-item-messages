from collections import OrderedDict
from django.contrib.messages.storage.base import Message as BaseMessage
from ..utils import get_msg_path
from ..utils import get_model_id
from ..utils import get_msg_id


class Message(BaseMessage):
    def __init__(self, msg_id, model_id, obj_id, level, message, extra_tags="", extra_data=None):
        super().__init__(level, message, extra_tags)
        self.id = msg_id
        self.model_id = model_id
        self.obj_id = obj_id
        self.extra_data = extra_data

    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return self.id == other.id


# FIXME: Make this class a dict type.
class StorageMixin:
    def _prepare_messages(self, messages):
        """
        _summary_
        """
        for model_msgs in messages.values():
            for obj_msgs in model_msgs.values():
                for msg in obj_msgs.values():
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

        # Prepare the queued_messages dictonary.
        model_id, obj_id = get_msg_path(obj)
        if not model_id in self._loaded_messages:
            self._loaded_messages[model_id] = dict()
        if not obj_id in self._loaded_messages[model_id]:
            self._loaded_messages[model_id][obj_id] = OrderedDict()

        # Create and add message.
        msg_id = get_msg_id(self._loaded_messages[model_id][obj_id])
        msg = Message(msg_id, model_id, obj_id, level, message, extra_tags, extra_data)
        self._loaded_messages[msg.model_id][msg.obj_id][msg.id] = msg

        return msg

    def update_message(self, msg_id, message, level=None, extra_tags="", extra_data=None):
        """
        _summary_

        :param str msg_id: _description_
        :param str message: _description_
        """
        msg = self.get(msg_id=msg_id)
        if msg:
            new_msg = Message(
                msg.id,
                msg.model_id,
                msg.obj_id,
                level or msg.level,
                message,
                extra_tags or msg.extra_tags,
                extra_data or msg.extra_data,
                )
            self._loaded_messages[msg.model_id][msg.obj_id][msg.id] = new_msg

    def get(self, model=None, obj=None, msg_id=None):
        """
        Get either all or model specific or object specific messages.
        """
        if msg_id:
            model_id, obj_id = msg_id.split(':')[:2]
            try:
                return self._loaded_messages.get(model_id, {}).get(obj_id, {})[msg_id]
            except KeyError:
                return None
        elif obj:
            model_id, obj_id = get_msg_path(obj)
            return self._loaded_messages.get(model_id, {}).get(obj_id, {})
        elif model:
            return self._loaded_messages.get(get_model_id(model), {})
        else:
            return self._loaded_messages

    def remove(self, model=None, obj=None, msg_id=None):
        """
        _summary_
        """
        if msg_id:
            model_id, obj_id = msg_id.split(':')[:2]
            try:
                del self._loaded_messages.get(model_id, {}).get(obj_id, {})[msg_id]
            except KeyError:
                pass
        elif obj:
            model_id, obj_id = get_msg_path(obj)
            try:
                del self._loaded_messages.get(model_id, {})[obj_id]
            except KeyError:
                pass
        elif model:
            try:
                del self._loaded_messages[get_model_id(model)]
            except KeyError:
                pass
        else:
            del self._loaded_data
