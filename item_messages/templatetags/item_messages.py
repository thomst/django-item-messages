from django.template.loader import render_to_string
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.contrib.admin.templatetags.admin_list import register
from django.contrib.admin.templatetags.admin_list import result_list
from django.utils.safestring import mark_safe


def item_messages_result_list(context, cl):
    """
    Inject item messages into the results returned by the original result_list.

    The items of this results are a list of table cell html snippets which are
    rendered within the change_list_results template. Since the table row is
    defined within this template, it's a little bit hacky to extend these html
    snippets by two table rows. But it prevents us from overwriting the complete
    change_list_results template which has no blocks at all.
    """
    results = result_list(cl)
    messages = context.get('item_messages', None)

    # Nothing to do if there are no messages for this request.
    if not messages:
        return results

    items = list()
    for item, obj in zip(results['results'], cl.result_list):
        obj_messages = messages.get(obj=obj)

        # Nothing to do if there are no messages for this object.
        if not obj_messages:
            items.append(item)

        # Else we render the messages html and append it to the item list.
        else:
            for msg in obj_messages.values():
                # Items are a list of table cells while their table row is set
                # by the change_list_result template. Since we inject additional
                # table rows to the list of table cells we start with a closing
                # row tag and end with an opening one. And we need to add two
                # rows to not break the css-even-odd logic of the result list.
                msg_html = f'<td colspan={len(item)}>{msg.html}</td>'
                msg_html = f'<tr class="item-message">{msg_html}</tr>'
                msg_html = f'</tr>{msg_html}<tr class="empty">'

                # Extend the item and add it to our items list.
                item.append(mark_safe(msg_html))
            items.append(item)

    results['results'] = items
    return results


# We overwrite the original result_list tag by using the register from
# admin_list templatetag library.
@register.tag(name="result_list")
def result_list_tag(parser, token):
    return InclusionAdminNode(
        parser,
        token,
        func=item_messages_result_list,
        template_name="change_list_results.html",
        takes_context=True,
    )
