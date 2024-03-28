from django.urls import path
from .views import SignUpView, UserLoginView, AgentLoginView, HotelViewSet, FlightViewSet, ViewViewSet, TravelPackageViewSet, PackageItemViewSet

urlpatterns = [
    path('hotels/', HotelViewSet.as_view({'get': 'list', 'post': 'create'}), name='hotel-list-create'),
    path('hotels/<int:pk>/', HotelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='hotel-detail'),
    
    path('flights/', FlightViewSet.as_view({'get': 'list', 'post': 'create'}), name='flight-list-create'),
    path('flights/<int:pk>/', FlightViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='flight-detail'),
    
    path('views/', ViewViewSet.as_view({'get': 'list', 'post': 'create'}), name='view-list-create'),
    path('views/<int:pk>/', ViewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='view-detail'),
    
    path('packages/', TravelPackageViewSet.as_view({'get': 'list', 'post': 'create'}), name='package-list-create'),
    path('packages/<int:pk>/', TravelPackageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='package-detail'),
    
    path('package-items/', PackageItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='packageitem-list-create'),
    path('package-items/<int:pk>/', PackageItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='packageitem-detail'),
    
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('agent/login/', AgentLoginView.as_view(), name='agent_login'),
]
