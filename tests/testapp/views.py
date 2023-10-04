
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from item_messages import api
from item_messages.constants import DEBUG
from item_messages.constants import DEFAULT_TAGS
from item_messages.api import update_message
from item_messages.api import remove_messages
from item_messages.api import get_messages



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
def update_message_view(request, msg_id, level, message, extra_tags="", extra_data=None):
    level = request.POST.get('level', 20)
    message = request.POST.get('message', None)
    extra_tags = request.POST.get('extra_tags', "")
    extra_data = request.POST.get('extra_data', None)
    update_message(request, msg_id, level, message, extra_tags, extra_data)

    model_key, _, _ = msg_id.split(':')
    app_label, _, model = model_key.split('.')
    url = reverse(f'admin:{app_label}_{model.lower()}_changelist')
    return HttpResponseRedirect(url)


@require_POST
def remove_messages_view(request, model=None, obj_id=None, msg_id=None):
    if obj_id:
        obj = model.objects.get(pk=obj_id)
        remove_messages(request, obj=obj)
    elif msg_id:
        remove_messages(request, msg_id=msg_id)
    else:
        remove_messages(request, model=model)

    ct = ContentType.objects.get_for_model(model)
    url = reverse(f'admin:{ct.app_label}_{ct.model}_changelist')
    return HttpResponseRedirect(url)


@require_GET
def get_messages_view(request, model=None, obj_id=None, msg_id=None):
    if obj_id:
        obj = model.objects.get(pk=obj_id)
        msgs = get_messages(request, obj=obj)
    elif msg_id:
        msgs = [get_messages(request, msg_id=msg_id)]
    else:
        msgs = get_messages(request, model=model)

    return render('testapp/messages.html', dict(msgs=msgs))