
from item_messages.api import remove_messages


def clear_item_messages(modeladmin, request, queryset):
    """
    An admin action to clear current item messages.
    """
    for obj in queryset.all():
        remove_messages(request, obj=obj)
