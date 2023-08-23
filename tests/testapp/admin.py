from django.contrib import admin
from .models import TestModel
from .actions import add_messages, clear_messages


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'one', 'two', 'three']
    actions = [add_messages, clear_messages]
