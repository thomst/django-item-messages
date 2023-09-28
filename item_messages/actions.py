
from item_messages.api import clear_messages


def clear_item_messages(modeladmin, request, queryset):
    """
    An admin action to clear current item messages.
    """
    for obj in queryset.all():
        clear_messages(request, obj)
