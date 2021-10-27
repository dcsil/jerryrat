from django.test import TestCase, Client
from django.views import *
from myapp.models import *
from myapp import urls
from django.urls import reverse, resolve
# Create your tests here.


class TestPageIntegrity(TestCase, Client):
    page_names = urls.page_names

    def test_page(self):
        client = Client()
        for i in self.page_names:
            print("Testing " + i)
            response = client.get(reverse(i))
            self.assertEquals(response.status_code, 200)
