from django.test import TestCase
from django.contrib.auth import get_user_model
from visa_payment.models import UserProfile, SuspiciousLogin

User = get_user_model()

class ModelsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234")

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user.username, "testuser")
        self.assertEqual(profile.failed_login_attempts, 0)
        self.assertFalse(profile.suspicious_warning)

    def test_suspicious_login(self):
        sl = SuspiciousLogin.objects.create(user=self.user, attempts=3, warning_issued=True)
        self.assertEqual(sl.attempts, 3)
        self.assertTrue(sl.warning_issued)
