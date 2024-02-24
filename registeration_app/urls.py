# registration_app/urls.py

from django.urls import path
from .views import SignUpView, UserLoginView, AgentLoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('agent/login/', AgentLoginView.as_view(), name='agent_login'),
]

