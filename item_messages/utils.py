from django.db.models import Model


def get_msg_path(obj):
    """
    _summary_

    :param _type_ obj: _description_
    :return _type_: _description_
    """
    return (get_model_id(obj), str(obj.id))


def get_model_id(obj_or_model):
    """
    _summary_

    :param _type_ obj_or_model: _description_
    :return _type_: _description_
    """
    if isinstance(obj_or_model, Model):
        model = type(obj_or_model)
    else:
        model = obj_or_model
    return f'{model.__module__}.{model.__name__}'