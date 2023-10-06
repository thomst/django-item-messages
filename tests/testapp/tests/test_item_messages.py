import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from testapp.management.commands.createtestdata import create_test_data
from testapp.models import TestModel
from item_messages.constants import DEFAULT_TAGS
from item_messages.storage.session import MessageDecoder
from item_messages.utils import get_msg_path
from ..utils import flatten_dict



UNICODE_STRING = 'ℋ ℌ ℍ,ℎ;ℏ ℐ ℑ ℒ ℓ'



class ItemMessagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.client.force_login(self.admin)
        self.changelist_url = reverse(f'admin:{TestModel._meta.app_label}_{TestModel._meta.model_name}_changelist')

    def add_messages(self):
        url_pattern = '/add_message/testmodel/{obj.id}/'
        msg_pattern = 'Message for {obj}.'
        msg_data = {
            'level': 20,
            'message': '',
            'extra_tags': '',
        }

        # A message for each object.
        for obj in TestModel.objects.all():
            data = msg_data.copy()
            data['message'] = msg_pattern.format(obj=obj)
            url = url_pattern.format(obj=obj)
            resp = self.client.post(url, data, follow=True)
            self.assertEqual(resp.status_code, 200)

        # Multiple messages for one object with different levels.
        msg_pattern = 'Message with level {level} for {obj}.'
        obj = TestModel.objects.get(pk=1)
        url = url_pattern.format(obj=obj)
        for level in DEFAULT_TAGS:
            data = msg_data.copy()
            data['message'] = msg_pattern.format(obj=obj, level=level)
            data['level'] = level
            resp = self.client.post(url, data, follow=True)
            self.assertEqual(resp.status_code, 200)

        messages = json.loads(self.client.session['_item_messages'], cls=MessageDecoder)
        return messages

    def test_add_messages(self):
        msgs = self.add_messages()

        # Check if all messages are rendered.
        resp = self.client.get(self.changelist_url)
        self.assertEqual(resp.status_code, 200)
        for msg in flatten_dict(msgs):
            self.assertIn(msg.id, resp.content.decode('utf8'))
            self.assertIn(msg.message, resp.content.decode('utf8'))

    def test_update_messages(self):
        url_pattern = '/update_message/{msg_id}/'

        msgs = self.add_messages()

        obj = TestModel.objects.get(pk=1)
        model_key, obj_key = get_msg_path(obj)
        for msg in flatten_dict(msgs[model_key][obj_key])[3:]:
            url = url_pattern.format(msg_id=msg.id)
            data = dict(
                message=f'[UPDATED] {msg.message}',
                level=msg.level,
            )
            resp = self.client.post(url, data, follow=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(data['message'], resp.content.decode('utf8'))

    def test_remove_messages(self):
        msgs = self.add_messages()
        obj = TestModel.objects.get(pk=1)
        model_key, obj_key = get_msg_path(obj)

        # Remove a message by msg-id.
        msg = [m for m in msgs[model_key][obj_key].values()][-1]
        url = f'/remove_messages/{msg.id}/'
        resp = self.client.post(url, dict(), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(msg.id, resp.content.decode('utf8'))
        self.assertNotIn(msg.message, resp.content.decode('utf8'))

        # Remove a message by model-key.
        url = '/remove_messages/testmodel/'
        resp = self.client.post(url, dict(), follow=True)
        for msg in flatten_dict(msgs[model_key]):
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(msg.id, resp.content.decode('utf8'))
            self.assertNotIn(msg.message, resp.content.decode('utf8'))

        # Remove a message by obj-key.
        url = f'/remove_messages/testmodel/{msg.obj_key}/'
        resp = self.client.post(url, dict(), follow=True)
        self.assertEqual(resp.status_code, 200)
        for msg in msgs[model_key][obj_key].values():
            self.assertNotIn(msg.id, resp.content.decode('utf8'))
            self.assertNotIn(msg.message, resp.content.decode('utf8'))

        # Remove all messages.
        url = '/remove_messages/'
        resp = self.client.post(url, dict(), follow=True)
        self.assertEqual(resp.status_code, 200)

        # Check if there are all gone.
        resp = self.client.get(self.changelist_url)
        self.assertEqual(resp.status_code, 200)
        for msg in flatten_dict(msgs):
            self.assertNotIn(msg.id, resp.content.decode('utf8'))
            self.assertNotIn(msg.message, resp.content.decode('utf8'))

    def test_get_messages(self):
        msgs = self.add_messages()
        obj = TestModel.objects.get(pk=1)
        model_key, obj_key = get_msg_path(obj)

        # Get a message by msg-id.
        msg = [m for m in msgs[model_key][obj_key].values()][-1]
        url = f'/get_messages/{msg.id}/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(msg.id, resp.content.decode('utf8'))
        self.assertIn(msg.message, resp.content.decode('utf8'))

        # Get a message by obj-key.
        url = f'/get_messages/testmodel/{obj_key}/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        for msg in msgs[model_key][obj_key].values():
            self.assertIn(msg.id, resp.content.decode('utf8'))
            self.assertIn(msg.message, resp.content.decode('utf8'))

        # Get a message by model-key.
        url = '/get_messages/testmodel/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        for msg in flatten_dict(msgs[model_key]):
            self.assertIn(msg.id, resp.content.decode('utf8'))
            self.assertIn(msg.message, resp.content.decode('utf8'))

        # Get all messages.
        url = '/get_messages/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        for msg in flatten_dict(msgs):
            self.assertIn(msg.id, resp.content.decode('utf8'))
            self.assertIn(msg.message, resp.content.decode('utf8'))

