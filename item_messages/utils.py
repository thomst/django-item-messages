from django.db.models import Model
from django.contrib.contenttypes.models import ContentType


def get_msg_key(obj_messages):
    """
    _summary_

    :param _type_ msg: _description_
    :return _type_: _description_
    """
    try:
        return str(int([id for id in obj_messages.keys()][-1]) + 1)
    except IndexError:
        return str(0)


def get_msg_path(obj):
    """
    _summary_

    :param _type_ obj: _description_
    :return _type_: _description_
    """
    return (get_model_key(obj), str(obj.id))


def get_model_key(obj_or_model):
    """
    _summary_

    :param _type_ obj_or_model: _description_
    :return _type_: _description_
    """
    if isinstance(obj_or_model, Model):
        model = type(obj_or_model)
    else:
        model = obj_or_model
    return str(ContentType.objects.get_for_model(model).id)
