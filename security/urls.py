from django.urls import path
from .views import LoginCustomView, SignUpView, DashboardView, ProfileView, ChangePasswordView

urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('security/', ChangePasswordView.as_view(), name='pass'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]