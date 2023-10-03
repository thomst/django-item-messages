from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html

from item_messages.api import add_message
from item_messages.api import get_messages
from item_messages.api import update_message
from .forms import AddMessageFrom
from .forms import UpdateMessageFrom


def add_messages(modeladmin, request, queryset):
    if 'add_messages' in request.POST:
        form = AddMessageFrom(request.POST)
    else:
        form = AddMessageFrom(initial={'level': 20})

    if form.is_valid():
        # add message
        msg = format_html('{msg}', msg=form.cleaned_data['message'])
        level = form.cleaned_data['level']
        for obj in queryset.all():
            add_message(request, obj, level, msg)

        return HttpResponseRedirect(request.get_full_path())
    else:
        return render(request, 'testapp/message_action.html', {
            'action': 'add_messages',
            'objects': queryset.order_by('pk'),
            'form': form,
            })


def update_message_by_id(modeladmin, request, queryset):
    msg_ids = []
    for obj in queryset.all():
        msgs = get_messages(request, obj=obj)
        for msg in msgs.values():
            msg_ids.append(msg.id)

    if 'update_message_by_id' in request.POST:
        form = UpdateMessageFrom(msg_ids, request.POST)
    else:
        form = UpdateMessageFrom(msg_ids, initial={'level': 20})

    if form.is_valid():
        # add message
        msg = format_html('{msg}', msg=form.cleaned_data['message'])
        level = form.cleaned_data['level']
        msg_id = form.cleaned_data['msg_id']
        update_message(request, msg_id, level, msg)

        return HttpResponseRedirect(request.get_full_path())
    else:
        return render(request, 'testapp/message_action.html', {
            'action': 'update_message_by_id',
            'objects': queryset.order_by('pk'),
            'form': form,
            })
