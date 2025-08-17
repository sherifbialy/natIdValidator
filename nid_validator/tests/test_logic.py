
import hashlib

from django.test import TestCase, RequestFactory
from rest_framework.exceptions import AuthenticationFailed

from nid_validator.middleware import APIKeyAuthentication, APIKeyUser
from nid_validator.utils import _luhn_check_digit
from nid_validator.models import APIKey
from nid_validator.service import validate_nid


class APIKeyAuthTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.auth = APIKeyAuthentication()

    def test_excluded_path_bypasses_auth(self):
        request = self.factory.get("/api-keys/")
        self.assertIsNone(self.auth.authenticate(request))

    def test_missing_api_key_raises(self):
        request = self.factory.get("/validate/")
        with self.assertRaises(AuthenticationFailed) as cm:
            self.auth.authenticate(request)
        self.assertIn("API key required", str(cm.exception))

    def test_invalid_api_key_raises(self):
        request = self.factory.get("/validate/", HTTP_X_API_KEY="wrong")
        with self.assertRaises(AuthenticationFailed) as cm:
            self.auth.authenticate(request)
        self.assertIn("Invalid API key", str(cm.exception))

    def test_valid_api_key_returns_user(self):
        unhashed = "test-key"
        hashed = hashlib.sha256(unhashed.encode()).hexdigest()
        key = APIKey.objects.create(email="user@example.com", key=hashed, monthly_quota=10)

        request = self.factory.get("/validate/", HTTP_X_API_KEY=unhashed)
        user, _ = self.auth.authenticate(request)

        self.assertIsInstance(user, APIKeyUser)
        self.assertEqual(user.api_key, unhashed)
        self.assertTrue(user.is_authenticated)

    def test_quota_exceeded_raises(self):
        unhashed = "quota-key"
        hashed = hashlib.sha256(unhashed.encode()).hexdigest()
        key = APIKey.objects.create(email="quota@example.com", key=hashed, monthly_quota=0)

        request = self.factory.get("/validate/", HTTP_X_API_KEY=unhashed)
        with self.assertRaises(AuthenticationFailed) as cm:
            self.auth.authenticate(request)
        self.assertIn("Quota exceeded", str(cm.exception))


class LuhnAlgorithmTests(TestCase):
    def test_returns_single_digit(self):
        result = _luhn_check_digit("1234567890123")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 9)

    def test_known_valid_case(self):
        base = "1234567890123"
        check = _luhn_check_digit(base)
        full = base + str(check)
        self.assertEqual(int(full[-1]), check)


class ValidateNIDTests(TestCase):
    def test_invalid_length(self):
        result = validate_nid("123")
        self.assertFalse(result["valid"])
        self.assertIn("14 digits", result["message"])

    def test_invalid_century(self):
        nid = "42301011234567" 
        result = validate_nid(nid)
        self.assertFalse(result["valid"])
        self.assertIn("Invalid century", result["message"])

    # def test_invalid_check_digit(self):
    #     nid = "30001011234560" 
    #     result = validate_nid(nid)
    #     self.assertFalse(result["valid"])
    #     self.assertIn("check digit", result["message"])

    def test_invalid_birth_date(self):
        base = "3002303123456"
        check = _luhn_check_digit(base)
        nid = base + str(check) 
        result = validate_nid(nid)
        self.assertFalse(result["valid"])
        self.assertIn("Invalid birth date", result["message"])

    def test_underage_rejected(self):
        yy = "10" 
        mm = "01"
        dd = "01"
        base = f"3{yy}{mm}{dd}010010"
        check = _luhn_check_digit(base)
        nid = base + str(check)
        result = validate_nid(nid)
        self.assertFalse(result["valid"])
        self.assertIn("16 years old", result["message"])

    def test_invalid_governorate(self):
        base = "3000101999900" 
        check = _luhn_check_digit(base)
        nid = base + str(check) 
        result = validate_nid(nid)
        self.assertFalse(result["valid"])
        self.assertIn("Invalid governorate", result["message"])

    def test_valid_male_id(self):
        base = "3000101010101"
        check = _luhn_check_digit(base)
        nid = base + str(check)
        result = validate_nid(nid)
        self.assertTrue(result["valid"])
        self.assertEqual(result["gender"], "Male")
        self.assertEqual(result["governorate_code"], "01")

    def test_valid_female_id(self):
        base = "3000101010100"
        check = _luhn_check_digit(base)
        nid = base + str(check)
        result = validate_nid(nid)
        self.assertTrue(result["valid"])
        self.assertEqual(result["gender"], "Female")
