import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from core.models import BaseModel, BaseModelWithAudit
from django.db import models

from users.models import UserProfile

User = get_user_model()


class TestBaseModel(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "core"
        managed = True


class TestBaseModelWithAudit(BaseModelWithAudit):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    class Meta:
        app_label = "core"
        managed = True


class BaseModelTest(TestCase):
    def test_base_model_abstract(self):
        """Test that BaseModel is abstract"""
        self.assertTrue(BaseModel._meta.abstract)

    def test_base_model_has_expected_fields(self):
        """Test that BaseModel has all expected fields"""
        field_names = [field.name for field in BaseModelWithAudit._meta.get_fields()]
        expected_fields = ["id", "created_at", "updated_at", "is_active", "is_deleted"]

        for field in expected_fields:
            self.assertIn(field, field_names)


class BaseModelWithAuditTest(TestCase):
    def test_base_model_with_audit_abstract(self):
        """Test that BaseModelWithAudit is abstract"""
        self.assertTrue(BaseModelWithAudit._meta.abstract)

    def test_base_model_with_audit_has_audit_fields(self):
        """Test that BaseModelWithAudit has all audit fields"""
        field_names = [field.name for field in BaseModelWithAudit._meta.get_fields()]

        self.assertIn("created_by", field_names)
        self.assertIn("updated_by", field_names)
        self.assertIn("deleted_by", field_names)
        self.assertIn("deleted_at", field_names)


class ModelImplementationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass@123"
        )

    def test_base_model_creation(self):
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
        self.assertIsInstance(self.user.id, uuid.UUID)

    def test_concrete_base_model_with_audit_creation(self):
        """Test creating a concrete instance of BaseModelWithAudit"""
        from django_currentuser.middleware import _set_current_user

        _set_current_user(self.user)
        profile = UserProfile.objects.create(
            user=self.user,
        )

        self.assertEqual(profile.created_by.email, self.user.email)
