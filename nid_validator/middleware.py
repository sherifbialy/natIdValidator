# core/authentication.py
import hashlib
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey


class APIKeyUser:
    def __init__(self, key):
        self.api_key = key
        self.is_authenticated = True  

class APIKeyAuthentication(BaseAuthentication):
    EXCLUDED_PREFIXES = [
        "/api-keys/",
    ]

    def authenticate(self, request):

        for prefix in self.EXCLUDED_PREFIXES:
            if request.path.startswith(prefix):
                return None  
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            raise AuthenticationFailed("API key required")

        hashed = hashlib.sha256(api_key.encode()).hexdigest()

        try:
            key_obj = APIKey.objects.get(key=hashed)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")


        if not key_obj.increment_usage() and request.path == "/validate/":
            print("Quota exceeded for this API key")
            raise AuthenticationFailed("Quota exceeded for this API key")

    
        return (APIKeyUser(api_key), None)

