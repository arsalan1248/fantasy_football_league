import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import UserProfile

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="john", email="john@example.com", password="Pass1234!"
        )
        self.assertIsNotNone(user.id)
        self.assertIsInstance(user.id, uuid.UUID)
        self.assertTrue(user.is_active)


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser", email="profile@example.com", password="Pass1234!"
        )

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user.id, self.user.id)
        self.assertTrue(hasattr(profile, "created_at"))

    def test_profile_photo_upload(self):
        photo_file = SimpleUploadedFile(
            name="test_image.jpg", content=b"file_content", content_type="image/jpeg"
        )
        profile = UserProfile.objects.create(user=self.user, profile_picture=photo_file)
        self.assertTrue(profile.profile_picture.name.endswith("test_image.jpg"))
