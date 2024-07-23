from django.test import TestCase, Client
from django.urls import reverse
from profiles.models import Profile

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.create(name='Test Profile')

    def test_profile_list_url(self):
        response = self.client.get(reverse('profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles_page.html')

    def test_detail_url(self):
        response = self.client.get(reverse('detail', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')

    def test_edit_url(self):
        response = self.client.get(reverse('edit', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_delete_url(self):
        response = self.client.get(reverse('delete', args=[self.profile.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile_list'))

    def test_add_profile_url(self):
        response = self.client.get(reverse('add_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_profile.html')