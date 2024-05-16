from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StockSymbol
from .serializers import *
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

def home(request):
    return render(request, 'index.html')

class StockSymbolCreateView(APIView):
    def post(self, request):
        serializer = StockSymbolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockSymbolListView(APIView):
    def get(self, request):
        symbols = StockSymbol.objects.filter(user=request.user)
        serializer = StockSymbolSerializer(symbols, many=True)
        return Response(serializer.data)
    
class StockSymbolDetailView(RetrieveUpdateDestroyAPIView):
    queryset = StockSymbol.objects.all()
    serializer_class = StockSymbolSerializer
    lookup_field = 'pk'

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors})
        
        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj)})

    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
