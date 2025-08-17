
from nid_validator.middleware import APIKeyAuthentication
from nid_validator.service import validate_nid
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import APIKey, NationalID
from .serializers import APIKeySerializer, NationalIDSerializer
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny



class NationalIDValidationView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        nid = request.data.get("nid")
        if not nid:
            return Response({"error": "You must submit an id"}, status=400)

        cached = cache.get(nid)
        if cached:
            return Response(cached)

        existing = NationalID.objects.filter(nid=nid).first()
        if existing:
            data = NationalIDSerializer(existing).data
            cache.set(nid, data, timeout=86400)
            return Response(data)

        data = validate_nid(nid)
        if not data["valid"]:
            return Response({"error": data["message"]}, status=400)
            

        NationalID.objects.create(
            nid=nid,
            birth_date=data["birth_date"],
            governorate_code=data["governorate_code"],
            gender=data["gender"]
        )
        cache.set(nid, data, timeout=86400)
        return Response(data)

    
class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    # permission_classes = [IsAdminUser] 

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        monthly_quota = request.data.get("monthly_quota", 1000)
        #check if email already exists
        if APIKey.objects.filter(email=email).exists():
            return Response({"error": "API key for this email already exists"}, status=400)
        if not email:
            return Response({"error": "Email is required"}, status=400)
        instance, unhashed = APIKey.create_with_email(email, None, monthly_quota)

        serializer = self.get_serializer(instance)
        data = serializer.data
        data["unhashed_key"] = unhashed
        return Response(data, status=201)

