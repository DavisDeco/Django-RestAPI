from django.test import TestCase

# Create your tests here.
# Create your tests here.
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTestCase(TestCase):
    def stUp(self):
        user = User.objects.create(username='Arifu', email='info@arifu.com')
        user.set_password('liver2pool')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username="Arifu")
        self.assertEqual(qs.count(),1)