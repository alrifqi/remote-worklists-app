__author__ = 'alrifqi'
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from Fetcher.models import Company, Source, Work


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','email', 'password')
        write_only_fields = ('password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class CompanySerializer(serializers.ModelSerializer):
    works = serializers.StringRelatedField(many=True)
    class Meta:
        model = Company
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    works = serializers.StringRelatedField(many=True)
    class Meta:
        model = Source
        fields = '__all__'


class WorkSerializer(serializers.ModelSerializer):
    source = SourceSerializer(

    )
# router = routers.DefaultRouter()