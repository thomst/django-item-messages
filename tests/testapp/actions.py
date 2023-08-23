from django.http import HttpResponseRedirect
from django.shortcuts import render

from item_messages.api import clear, add_message
from .forms import MessageFrom


def add_messages(modeladmin, request, queryset):
    if 'add_messages' in request.POST:
        form = MessageFrom(request.POST)
    else:
        form = MessageFrom()

    if form.is_valid():
        # add message
        data = form.cleaned_data
        for obj in queryset.all():
            add_message(request, data['level'], obj, data['message'])

        return HttpResponseRedirect(request.get_full_path())
    else:
        return render(request, 'testapp/message.html', {
            'objects': queryset.order_by('pk'),
            'form': form,
            })


def clear_messages(modeladmin, request, queryset):
    for obj in queryset.all():
        clear(request, obj)
