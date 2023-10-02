import json
from collections import OrderedDict
from django.contrib.messages.storage.session import SessionStorage as BaseSessionStorage
from django.contrib.messages.storage.cookie import MessageEncoder as BaseMessageEncoder
from django.contrib.messages.storage.cookie import MessageDecoder as BaseMessageDecoder
from django.utils.safestring import SafeData, mark_safe
from .base import StorageMixin
from .base import Message


class MessageEncoder(BaseMessageEncoder):
    """
    Compactly serialize instances of the ``Message`` class as JSON.
    """
    ordered_dict_key = '__json_ordered_dict'

    def default(self, obj):
        if isinstance(obj, Message):
            is_safedata = 1 if isinstance(obj.message, SafeData) else 0
            message = [self.message_key, is_safedata, obj.key, obj.model_key, obj.obj_key, obj.level, obj.message]
            if obj.extra_tags:
                message.append(obj.extra_tags)
            if obj.extra_data:
                message.append(obj.extra_data)
            return message
        if isinstance(obj, OrderedDict):
            ordered_dict = [self.ordered_dict_key]
            ordered_dict.append((k, self.default(v)) for k, v in obj.items())
            return ordered_dict
        return super().default(obj)


class MessageDecoder(BaseMessageDecoder):
    """
    Decode JSON that includes serialized ``Message`` instances.
    """
    def __init__(self, *args, **kwargs):
        kwargs['object_pairs_hook'] = OrderedDict
        super().__init__(*args, **kwargs)

    def process_messages(self, obj):
        if isinstance(obj, list) and obj:
            if obj[0] == MessageEncoder.message_key:
                if obj[1]:
                    obj[6] = mark_safe(obj[6])
                return Message(*obj[2:])

            if obj[0] == MessageEncoder.ordered_dict_key:
                return OrderedDict(((k, self.process_messages(v)) for k, v in obj[1:]))

            else:
                return [self.process_messages(item) for item in obj]

        if isinstance(obj, dict):
            return {key: self.process_messages(value) for key, value in obj.items()}

        return obj


class SessionStorage(StorageMixin, BaseSessionStorage):
    """
    Store messages in the session (that is, django.contrib.sessions).
    """
    session_key = "_item_messages"

    def serialize_messages(self, messages):
        encoder = MessageEncoder()
        return encoder.encode(messages)

    def deserialize_messages(self, data):
        if data and isinstance(data, str):
            return json.loads(data, cls=MessageDecoder)
        return data