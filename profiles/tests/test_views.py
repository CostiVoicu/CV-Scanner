from django.test import TestCase, Client
from django.urls import reverse
from profiles.models import Profile, KeyWord

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.create(name='Test Profile')
        self.keyword = KeyWord.objects.create(profile=self.profile, name='Test Keyword', value=5)

    def test_profiles_view(self):
        response = self.client.get(reverse('profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles_page.html')

        self.assertIn('profiles_list', response.context)
        profiles_list = list(response.context['profiles_list'])
        profiles_repr = [repr(profile) for profile in profiles_list]

        expected_repr = [repr(self.profile)]

        self.assertListEqual(profiles_repr, expected_repr)

    def test_profiles_details_view(self):
        response = self.client.get(reverse('detail', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertIn('profile', response.context)
        self.assertIn('keywords', response.context)
        self.assertEqual(response.context['profile'], self.profile)
        
        keywords_list = list(response.context['keywords'])
        keywords_repr = [repr(keyword) for keyword in keywords_list]
        expected_repr = [repr(self.keyword)]

        self.assertEqual(keywords_repr, expected_repr)

    def test_add_profile_view_get(self):
        response = self.client.get(reverse('add_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_profile.html')
        self.assertIn('profile_form', response.context)
        self.assertIn('keyword_formset', response.context)

    def test_add_profile_view_post(self):
        post_data = {
            'name': 'Test Profile',  
            'keywords-TOTAL_FORMS': '1',  
            'keywords-INITIAL_FORMS': '0',  
            'keywords-MIN_NUM_FORMS': '0',  
            'keywords-MAX_NUM_FORMS': '1000',  
            'keywords-0-name': 'keyword1', 
            'keywords-0-value': '10',
        }
        response = self.client.post(reverse('add_profile'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(name='Test Profile').exists())

    def test_delete_profile_view(self):
        response = self.client.post(reverse('delete', args=[self.profile.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile_list'))
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())

    def test_edit_profile_view_get(self):
        response = self.client.get(reverse('edit', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIn('profile_form', response.context)
        self.assertIn('keyword_formset', response.context)
        self.assertIn('profile', response.context)
        self.assertEqual(response.context['profile'], self.profile)

    def test_edit_profile_view_post(self):
        post_data = {
            'name': 'Updated Profile',  
            'keywords-TOTAL_FORMS': '1',  
            'keywords-INITIAL_FORMS': '1',  
            'keywords-MIN_NUM_FORMS': '0',  
            'keywords-MAX_NUM_FORMS': '1000',
            'keywords-0-id': self.keyword.id,
            'keywords-0-name': 'Updated Keyword', 
            'keywords-0-value': 12
        }
        response = self.client.post(reverse('edit', args=[self.profile.id]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.keyword.refresh_from_db()
        self.assertEqual(self.profile.name, 'Updated Profile')
        self.assertEqual(self.keyword.value, 12)
        self.assertEqual(self.keyword.name, 'Updated Keyword')