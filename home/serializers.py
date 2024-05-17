from rest_framework import serializers
from .models import StockSymbol
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        return user


class StockSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockSymbol
        fields = '__all__'
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
