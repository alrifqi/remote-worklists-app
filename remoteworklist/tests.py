import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory


class LoginTestCase(TestCase):
    def login_with_right_data(self):
        factory = APIRequestFactory()
        request = factory.post('/auth', json.dumps({'username': 'tes2', 'password': 'tes2'}), content_type='application/json')

