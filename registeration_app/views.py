from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import User,Agent
from .serializers import UserSerializer,AgentSerializer
from rest_framework import viewsets
from .models import Hotel, Flight, View, TravelPackage, PackageItem
from .serializers import HotelSerializer, FlightSerializer, ViewSerializer, TravelPackageSerializer, PackageItemSerializer

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
    

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class ViewViewSet(viewsets.ModelViewSet):
    queryset = View.objects.all()
    serializer_class = ViewSerializer

class TravelPackageViewSet(viewsets.ModelViewSet):
    queryset = TravelPackage.objects.all()
    serializer_class = TravelPackageSerializer

class PackageItemViewSet(viewsets.ModelViewSet):
    queryset = PackageItem.objects.all()
    serializer_class = PackageItemSerializer