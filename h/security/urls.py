
from django.urls import path, include
from .views import LoginCustomView, SignUpView, ProfileView, ChangePasswordView, LogoutView, \
    Forget
from django.urls import path
from .views import LoginCustomView, SignUpView, ProfileView, ChangePasswordView, LogoutView

urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('security/', ChangePasswordView.as_view(), name='pass'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
