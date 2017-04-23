from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token

from Fetcher.models import Company, Work, Source
from .serializers import UserSerializer, CompanySerializer, SourceSerializer

# Create your views here.
class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CompanyApi(APIView):
    permission_classes = ((IsAuthenticated, ))

    def get(self, pk):
        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(JSONRenderer().render(serializer.data))


class SourceApi(APIView):
    permission_classes = ((IsAuthenticated, ))

    def get(self):
        queryset = Source.objects.all()
        serializer = SourceSerializer(queryset, many=True)
        return Response(JSONRenderer().render(serializer.data))