
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from nid_validator.models import NationalID, APIKey
from nid_validator.utils import _luhn_check_digit
import hashlib

class NationalIDValidationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        instance, unhashed = APIKey.create_with_email(email="test@test.com", monthly_quota=1000)

        self.client.credentials(HTTP_X_API_KEY=unhashed)


        self.valid_base = "3000101010100"
        self.valid_check = _luhn_check_digit(self.valid_base)
        self.valid_nid = self.valid_base + str(self.valid_check)

    def test_missing_nid_returns_400(self):
        response = self.client.post("/validate/", data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("must submit an id", response.data["error"])

    def test_invalid_nid_returns_400(self):
        response = self.client.post("/validate/", data={"nid": "123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("14 digits", response.data["error"])

    def test_valid_nid_creates_record(self):
        response = self.client.post("/validate/", data={"nid": self.valid_nid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nid"], self.valid_nid)

    def test_existing_nid_uses_cache_or_db(self):

        NationalID.objects.create(
            nid=self.valid_nid,
            birth_date="2000-01-01",
            governorate_code="01",
            gender="Male"
        )
        response = self.client.post("/validate/", data={"nid": self.valid_nid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nid"], self.valid_nid)


class APIKeyViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = "/api-keys/"

    def test_create_api_key_requires_email(self):
        response = self.client.post(self.create_url, data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email is required", response.data["error"])

    def test_create_api_key_success(self):
        response = self.client.post(self.create_url, data={"email": "user@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("unhashed_key", response.data)
        self.assertTrue(APIKey.objects.filter(email="user@example.com").exists())

    def test_create_api_key_duplicate_email(self):
        APIKey.objects.create(email="user@example.com", key="dummy", monthly_quota=1000)
        response = self.client.post(self.create_url, data={"email": "user@example.com"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", response.data["error"])
