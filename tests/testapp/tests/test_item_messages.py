from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from testapp.management.commands.createtestdata import create_test_data
from testapp.models import TestModel
from item_messages.constants import DEFAULT_TAGS


UNICODE_STRING = 'ℋ ℌ ℍ,ℎ;ℏ ℐ ℑ ℒ ℓ'



class ItemMessagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.client.force_login(self.admin)
        self.changelist_url = reverse(f'admin:{TestModel._meta.app_label}_{TestModel._meta.model_name}_changelist')

    def test_add_messages(self):
        msgs = []
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
            msgs.append(data['message'])
            url = url_pattern.format(obj=obj)
            resp = self.client.post(url, data, follow=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(data['message'], resp.content.decode('utf8'))

        # Multiple messages for one object with different levels.
        msg_pattern = 'Message with level {level} for {obj}.'
        obj = TestModel.objects.get(pk=1)
        url = url_pattern.format(obj=obj)
        for level in DEFAULT_TAGS.keys():
            data = msg_data.copy()
            data['message'] = msg_pattern.format(obj=obj, level=level)
            msgs.append(data['message'])
            data['level'] = level
            resp = self.client.post(url, data, follow=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(data['message'], resp.content.decode('utf8'))

        # Check if all messages are rendered.
        resp = self.client.get(self.changelist_url)
        self.assertEqual(resp.status_code, 200)
        for msg in msgs:
            self.assertIn(msg, resp.content.decode('utf8'))
