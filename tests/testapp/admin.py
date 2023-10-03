from django.contrib import admin
from item_messages.actions import clear_item_messages
from .models import TestModel
from .actions import add_messages
from .actions import update_message_by_id


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'one', 'two', 'three']
    actions = [add_messages, update_message_by_id, clear_item_messages]
