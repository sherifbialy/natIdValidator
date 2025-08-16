
from nid_validator.middleware import APIKeyAuthentication
from nid_validator.service import validate_nid
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import APIKey, NationalID
from .serializers import APIKeySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny



class NationalIDValidationView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):

        if not request.data:
            return Response({"error": "You must submit data"}, status=400)
        
        nid = request.data.get("nid")
        if not nid:
            return Response({"error": "You must submit an id"}, status=400)

        existing = NationalID.objects.filter(nid=nid).first()
        if existing:
            return Response({
                "valid": True,
                "birth_date": existing.birth_date,
                "governorate_code": existing.governorate_code,
                "gender": existing.gender

            })

        data = validate_nid(nid)
        if not data["valid"]:
            return Response({"error": data["message"]}, status=400)
            
        NationalID.objects.create(
            nid=nid,
            birth_date=data["birth_date"],
            governorate_code=data["governorate_code"],
            gender=data["gender"]
        )
        return Response(data, status=201)
    
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

