from django.contrib import admin
from item_messages.api import add_message
from item_messages.api import update_message
from .models import TestModel
from item_messages import INFO, ERROR


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id']

    def changelist_view(self, request, extra_context=None):
        objs = TestModel.objects.filter(pk__in=[1, 3, 5, 6])
        for obj in objs:
            update_message(request, INFO, obj, str(obj))
            add_message(request, ERROR, obj, str(obj))

        return super().changelist_view(request, extra_context)
