from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.base import Model as Model
from django.views.generic import View
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView, GenericAPIView
from django.db.models.base import Model as Model
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.views import APIView
from .serializer import Userserializer, UpdatePassSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK


class LoginCustomView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            email = data.get('email')
            password = data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user=user)
                return redirect('/')
            raise object
        except Exception:
            context = {
                'error': 'Invalid email address and password', 'email': email}
            return render(request, template_name=self.template_name, context=context)


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone = data.get('phone')
            user = User.objects.create(
                email=email, first_name=first_name, last_name=last_name,
                phone=phone
            )
            user.set_password(password)
            user.save()
            login(request, user=user)
            return redirect('/')
        except Exception:
            context = {
                'error': 'User already registered with this email address', "email": email}
            return render(request, template_name=self.template_name, context=context)


class HybridViewMixin:

    def dispatch(self, request, *args, **kwargs):
        if 'text/html' in request.headers.get('Accept', ''):
            return self.render_html(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)

    def render_html(self, request, *args, **kwargs):
        raise NotImplementedError("render_html method must be implemented")


class ProfileView(HybridViewMixin, RetrieveUpdateAPIView):
    serializer_class = Userserializer
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user

    def render_html(self, request, *args, **kwargs):
        if str(request.user) != 'AnonymousUser':
            user = self.get_object()
            serializer = self.serializer_class(user)
            return render(request, self.template_name, context={**serializer.data})
        else:
            return redirect('/login')


class ChangePasswordView(HybridViewMixin, UpdateAPIView):
    serializer_class = UpdatePassSerializer
    template_name = 'changepass.html'

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        data = request.data
        if request.user.check_password(data.get('currentPass')):
            if data.get('newPass') == data.get('newPass2'):
                request.user.set_password(data.get('newPass'))
                request.user.save()
                logout(request)
                return Response(status=HTTP_200_OK)
        return Response(status=HTTP_403_FORBIDDEN)

    def render_html(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/account/login')

class Forget(SuccessMessageMixin, PasswordResetView):
    template_name = 'forget.html'
    email_template_name = 'resetmail.html'
    subject_template_name = 'Password reset'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
