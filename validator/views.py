from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NationalID
from .serializers import NationalIDSerializer
from .utils import validate_nid

class NationalIDValidationView(APIView):
    def post(self, request):
        nid = request.data.get("nid")
        if not nid:
            return Response({"error": "You must submit an id"}, status=400)

        existing = NationalID.objects.filter(nid=nid).first()
        if existing:
            return Response(NationalIDSerializer(existing).data)

        try:
            data = validate_nid(nid)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        saved = NationalID.objects.create(
            nid=nid,
            birth_date=data["birth_date"],
            governorate_code=data["governorate_code"],
            gender=data["gender"]
        )
        return Response(NationalIDSerializer(saved).data, status=201)

