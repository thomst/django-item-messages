
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from item_messages.storage.base import Message
from item_messages import api
from item_messages.constants import DEBUG
from item_messages.constants import DEFAULT_TAGS
from item_messages.api import update_message
from item_messages.api import remove_messages
from item_messages.api import get_messages
from .utils import flatten_dict



@require_POST
def add_message_view(request, obj_id, model):
    obj = model.objects.get(pk=obj_id)
    level = request.POST.get('level', '20')
    message = request.POST.get('message', None)
    extra_tags = request.POST.get('extra_tags', "")
    # extra_data = request.POST.get('extra_data', None)

    # Set level to debug to be sure every message is added.
    api.set_level(request, DEBUG)

    # We use the shortcut api functions to get a better coverage.
    tag = DEFAULT_TAGS[int(level)]
    func = getattr(api, tag)
    func(request, obj, message, extra_tags)

    ct = ContentType.objects.get_for_model(model)
    url = reverse(f'admin:{ct.app_label}_{ct.model}_changelist')
    return HttpResponseRedirect(url)


@require_POST
def update_message_view(request, msg_id):
    level = request.POST.get('level', 20)
    message = request.POST.get('message', None)
    extra_tags = request.POST.get('extra_tags', "")
    extra_data = request.POST.get('extra_data', None)
    update_message(request, msg_id, level, message, extra_tags, extra_data)

    model_key, _, _ = msg_id.split(Message.id_separator)
    ct = ContentType.objects.get_for_id(model_key)
    url = reverse(f'admin:{ct.app_label}_{ct.model}_changelist')
    return HttpResponseRedirect(url)


@require_POST
def remove_messages_view(request, model=None, obj_id=None, msg_id=None):
    if obj_id:
        obj = model.objects.get(pk=obj_id)
        remove_messages(request, obj=obj)
    elif msg_id:
        remove_messages(request, msg_id=msg_id)
    elif model:
        remove_messages(request, model=model)
    else:
        remove_messages(request)
        url = '/admin/'
        return HttpResponseRedirect(url)

    ct = ContentType.objects.get_for_model(model)
    url = reverse(f'admin:{ct.app_label}_{ct.model}_changelist')
    return HttpResponseRedirect(url)


@require_GET
def get_messages_view(request, model=None, obj_id=None, msg_id=None):
    if obj_id:
        obj = model.objects.get(pk=obj_id)
        msgs = get_messages(request, obj=obj)
        msgs = flatten_dict(msgs)
    elif msg_id:
        msgs = [get_messages(request, msg_id=msg_id)]
    elif model:
        msgs = get_messages(request, model=model)
        msgs = flatten_dict(msgs)
    else:
        msgs = get_messages(request)
        msgs = flatten_dict(msgs)

    return render(request, 'testapp/messages.html', dict(msgs=msgs))
