from django.test import TestCase
from profiles.models import Profile, KeyWord

class TestProfileModel(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(name='Test Profile')

    def test_profile_creation(self):
        self.assertEqual(self.profile.name, 'Test Profile')
        self.assertEqual(str(self.profile), 'Test Profile')

    def test_profile_name_max_lenght(self):
        max_lenght = self.profile._meta.get_field('name').max_length
        self.assertEqual(max_lenght, 50)
    
class TestKeyWordModel(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(name='Test Profile')
        self.keyword = KeyWord.objects.create(profile=self.profile, name='Test KeyWord', value=10)

    def test_keyword_creation(self):
        self.assertEqual(self.keyword.profile, self.profile)
        self.assertEqual(self.keyword.name, 'Test KeyWord')
        self.assertEqual(self.keyword.value, 10)
        self.assertEqual(str(self.keyword), 'Test KeyWord (10)')

    def test_keyword_name_max_lenght(self):
        max_lenght = self.keyword._meta.get_field('name').max_length
        self.assertEqual(max_lenght, 100)

    def test_keyword_value_integer(self):
        self.assertIsInstance(self.keyword.value, int)