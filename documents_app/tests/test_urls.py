from django.test import SimpleTestCase
from django.urls import reverse, resolve
from documents_app.views import scanner

class TestUrls(SimpleTestCase):

    def test_scanner_url_is_resolved(self):
        url = reverse('scanner')
        self.assertEquals(resolve(url).func, scanner)