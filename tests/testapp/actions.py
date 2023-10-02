from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html

from item_messages.api import add_message
from .forms import MessageFrom


def add_messages(modeladmin, request, queryset):
    if 'add_messages' in request.POST:
        form = MessageFrom(request.POST)
    else:
        form = MessageFrom(initial={'level': 20})

    if form.is_valid():
        # add message
        msg = format_html('{msg}', msg=form.cleaned_data['message'])
        level = form.cleaned_data['level']
        for obj in queryset.all():
            add_message(request, obj, level, msg)

        return HttpResponseRedirect(request.get_full_path())
    else:
        return render(request, 'testapp/message.html', {
            'objects': queryset.order_by('pk'),
            'form': form,
            })
