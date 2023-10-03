from django import forms
from item_messages.constants import DEFAULT_TAGS


class AddMessageFrom(forms.Form):
    message = forms.CharField(widget=forms.Textarea())
    level = forms.ChoiceField(choices=[(k, v) for k, v in DEFAULT_TAGS.items()])


class UpdateMessageFrom(forms.Form):
    def __init__(self, msg_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['msg_id'].choices = [(id, id) for id in msg_ids]

    message = forms.CharField(widget=forms.Textarea())
    level = forms.ChoiceField(choices=[(k, v) for k, v in DEFAULT_TAGS.items()])
    msg_id = forms.ChoiceField(choices=[])
