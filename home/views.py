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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics

def home(request):
    return render(request, 'index.html')

class StockSymbolAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):        
        symbol_obj = StockSymbol.objects.filter(user=request.user)
        serializer = StockSymbolSerializer(symbol_obj, many=True)
        return Response({'status': 200, 'payload': serializer.data})

    def post(self, request):
        user = request.user
        symbols = StockSymbol.objects.create(user=user, symbol=request.data['symbol'], description=request.data['description'], currency=request.data['currency'], type=request.data['type'])
        serializer = StockSymbolSerializer(symbols)
        return Response({'data': serializer.data})

    def delete(self, request):
        try:
            id = request.data['id']
            symbol_obj = StockSymbol.objects.get(id = id)
            symbol_obj.delete()
            return Response({'status': 200, 'message': 'deleted'})
        except Exception as e:
            return Response({'status': 403, 'message': 'invalid id'})
        
class StockSymbolListCreateView(generics.ListCreateAPIView):
    queryset = StockSymbol.objects.all()
    serializer_class = StockSymbolSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
