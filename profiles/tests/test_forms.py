from django.test import TestCase
from profiles.models import Profile
from profiles.forms import ProfileForm, KeyWordForm, KeyWordFormSet

class TestProfileForm(TestCase):
    def test_profile_form_valid(self):
        form = ProfileForm(data={'name': 'Test Profile'})
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid(self):
        form = ProfileForm(data={'name': ''})
        self.assertFalse(form.is_valid())

class TestKeyWordForm(TestCase):
    def test_keyword_form_valid(self):
        form = KeyWordForm(data={'name': 'Test Keyword', 'value': 10})
        self.assertTrue(form.is_valid())

    def test_keyword_form_invalid(self):
        form = KeyWordForm(data={'name': '', 'value': 10})
        self.assertFalse(form.is_valid())
        form = KeyWordForm(data={'name': 'Test Keyword', 'value': ''})
        self.assertFalse(form.is_valid())

class TestKeyWordFormSet(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(name='Test Profile')

    def test_keyword_formset_valid(self):
        formset_data = {
            'keywords-TOTAL_FORMS': '1',  
            'keywords-INITIAL_FORMS': '0',  
            'keywords-MIN_NUM_FORMS': '0',  
            'keywords-MAX_NUM_FORMS': '1000',
            'keywords-0-name': 'Test Keyword', 
            'keywords-0-value': '10'
        }
        formset = KeyWordFormSet(data=formset_data, instance=self.profile)
        self.assertTrue(formset.is_valid())

    def test_keyword_formset_invalid(self):
        formset_data = {
            'keywords-TOTAL_FORMS': '1',  
            'keywords-INITIAL_FORMS': '0',  
            'keywords-MIN_NUM_FORMS': '0',  
            'keywords-MAX_NUM_FORMS': '1000',
            'keywords-0-name': '', 
            'keywords-0-value': '10'
        }
        formset = KeyWordFormSet(data=formset_data, instance=self.profile)
        self.assertFalse(formset.is_valid())