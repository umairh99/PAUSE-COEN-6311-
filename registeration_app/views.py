from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import User,Agent
from .serializers import UserSerializer,AgentSerializer

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AgentLoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access agent login
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        agent = Agent.objects.filter(email=email, password=password).first()
        if agent:
            serializer = AgentSerializer(agent)
            return Response(serializer.data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)