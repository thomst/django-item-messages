from collections import OrderedDict
from django.template.loader import render_to_string
from django.contrib.messages.storage.base import Message as BaseMessage
from ..utils import get_msg_path
from ..utils import get_model_key
from ..utils import get_msg_key


class Message(BaseMessage):
    """
    _summary_
    """

    #: Separator character to build the message id.
    id_separator = '_'

    def __init__(self, msg_key, model_key, obj_key, level, message, extra_tags="", extra_data=None):
        super().__init__(level, message, extra_tags)
        self.key = msg_key
        self.model_key = model_key
        self.obj_key = obj_key
        self.extra_data = extra_data

    @property
    def id(self):
        return f'{self.model_key}{self.id_separator}{self.obj_key}{self.id_separator}{self.key}'

    @property
    def html(self):
        return render_to_string('item_messages/item_message.html', {'msg': self})

    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return self.key == other.key


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
        model_key, obj_key = get_msg_path(obj)
        if not model_key in self._loaded_messages:
            self._loaded_messages[model_key] = dict()
        if not obj_key in self._loaded_messages[model_key]:
            self._loaded_messages[model_key][obj_key] = OrderedDict()

        # Create and add message.
        msg_key = get_msg_key(self._loaded_messages[model_key][obj_key])
        msg = Message(msg_key, model_key, obj_key, level, message, extra_tags, extra_data)
        self._loaded_messages[msg.model_key][msg.obj_key][msg.key] = msg

        return msg.id

    def update_message(self, msg_id, level=None, message="", extra_tags="", extra_data=None):
        """
        _summary_

        :param str msg_key: _description_
        :param str message: _description_
        """
        msg = self.get(msg_id=msg_id)
        if msg:
            new_msg = Message(
                msg.key,
                msg.model_key,
                msg.obj_key,
                level or msg.level,
                message or msg.message,
                extra_tags or msg.extra_tags,
                extra_data or msg.extra_data,
                )
            self._loaded_messages[msg.model_key][msg.obj_key][msg.key] = new_msg

    def get(self, model=None, obj=None, msg_id=None):
        """
        Get either all or model specific or object specific messages.
        """
        if msg_id:
            model_key, obj_key, msg_key = msg_id.split(Message.id_separator)
            try:
                return self._loaded_messages.get(model_key, {}).get(obj_key, {})[msg_key]
            except KeyError:
                return None
        elif obj:
            model_key, obj_key = get_msg_path(obj)
            return self._loaded_messages.get(model_key, {}).get(obj_key, {})
        elif model:
            return self._loaded_messages.get(get_model_key(model), {})
        else:
            return self._loaded_messages

    def remove(self, model=None, obj=None, msg_id=None):
        """
        _summary_
        """
        if msg_id:
            model_key, obj_key, msg_key = msg_id.split(Message.id_separator)
            try:
                del self._loaded_messages.get(model_key, {}).get(obj_key, {})[msg_key]
            except KeyError:
                pass
        elif obj:
            model_key, obj_key = get_msg_path(obj)
            try:
                del self._loaded_messages.get(model_key, {})[obj_key]
            except KeyError:
                pass
        elif model:
            try:
                del self._loaded_messages[get_model_key(model)]
            except KeyError:
                pass
        else:
            self._loaded_messages
            del self._loaded_data
