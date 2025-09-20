from io import BytesIO
from PIL import Image
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def generate_test_image(format="JPEG", color=(255, 0, 0)):
    """Generate a simple in-memory image."""
    file = BytesIO()
    image = Image.new("RGB", (100, 100), color)
    image.save(file, format=format)
    file.seek(0)
    return file.getvalue()

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Pass1234!"
        }
        url = reverse("user-register")
        self.registration_response = self.client.post(url, payload)

        self.user = User.objects.get(email="newuser@example.com")

    def test_user_registration(self):
        
        self.assertEqual(self.registration_response.status_code, 201)
        self.assertEqual(self.registration_response.data["email"], "newuser@example.com")

    def test_user_profile_update_with_photo(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.client.force_authenticate(user=self.user)
        photo_file = SimpleUploadedFile(
            "update.jpg",
            generate_test_image(),
            content_type="image/jpeg"
        )
        response = self.client.patch(
            reverse("profile-me"),
            {"profile_picture": photo_file},
            format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("profile_picture", response.data)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        self.user.profile.bio = "test"
        self.user.profile.save()
        response = self.client.get(
            reverse("profile-me"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data["bio"], "test")
