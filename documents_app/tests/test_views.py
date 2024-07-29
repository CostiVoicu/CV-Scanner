from django.test import TestCase, Client
from django.urls import reverse
from profiles.models import Profile, KeyWord
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock
import base64
from documents_app.views import convertor_to_custom_format

class TestView(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(name="Test Profile")
        KeyWord.objects.create(profile=self.profile, name="test", value=3)

        self.client = Client()
        self.url = reverse('scanner')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents_page.html')
        self.assertIn('job_profiles', response.context)
        self.assertIn('count_error', response.context)
        self.assertQuerysetEqual(response.context['job_profiles'], [self.profile])

    @patch('documents_app.views.convertor_to_custom_format')
    @patch('documents_app.views.get_top_doc')
    def test_post_request(self, mock_get_top_doc, mock_convertor_to_custom_format):
        mock_convertor_to_custom_format.return_value = {'test': 'test_value'}
        mock_pdf_file = MagicMock()
        mock_pdf_file.read.return_value = b"test content"
        mock_get_top_doc.return_value = [mock_pdf_file]

        test_file = SimpleUploadedFile("document.pdf", b"test content", content_type="pdf")

        response = self.client.post(self.url, {
            'persons_count': 1,
            'job_profile': self.profile.id,
            'documents': [test_file]
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results_page.html')

        self.assertIn('file_data_urls', response.context)
        self.assertEqual(len(response.context['file_data_urls']), 1)
        expected_data_url = f"data:application/pdf;base64,{base64.b64encode(b'test content').decode('utf-8')}"
        self.assertEqual(response.context['file_data_urls'][0], expected_data_url)

    def test_post_request_invalid_profile(self):
        test_file = SimpleUploadedFile("document.pdf", b"test content", content_type="pdf")

        response = self.client.post(self.url, {
            'persons_count': 1,
            'job_profile': 999,
            'documents': [test_file]
        })

        self.assertEqual(response.status_code, 404)

    def test_convertor_to_custom_format(self):
        input_data = [
            {'name': 'python', 'value': 10},
            {'name': 'django', 'value': 8},
        ]
        expected_output = {
            'python': 10,
            'django': 8,
        }
        result = convertor_to_custom_format(input_data)
        self.assertEqual(result, expected_output)