# core/throttling.py
from rest_framework.throttling import SimpleRateThrottle

class APIKeyRateThrottle(SimpleRateThrottle):
    scope = "apikey"

    def get_cache_key(self, request, view):
        if not hasattr(request.user, "api_key"):
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": request.user.api_key
        }
