from django.contrib import admin
from item_messages.actions import clear_item_messages
from .models import TestModel
from .actions import add_messages


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'one', 'two', 'three']
    actions = [add_messages, clear_item_messages]
