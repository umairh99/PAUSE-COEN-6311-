from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from datetime import datetime, date
from django.template import RequestContext

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


from .models import UserProfile


@csrf_protect
def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if not (username and name and email and phone and dob and pass1 and pass2):
            return render(request, 'signup.html', {'error_message': "Please fill in all the fields."})

        if pass1 != pass2:
            return render(request, 'signup.html', {'error_message': "Passwords do not match. Please try again."})

        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        if dob_date > date.today():
            return render(request, 'signup.html', {'error_message': "Date of birth cannot be in the future."})

        else:
            try:
                # Attempt to create a new user
                my_user = User.objects.create_user(username=username, email=email, password=pass1)
                my_user.name = name
                my_user.save()

                # Create a UserProfile instance for the new user
                UserProfile.objects.create(user=my_user, phone=phone, dob=dob)

                return render(request, 'signup_success.html', {'message': "Signup successful. You can now log in."})
            except IntegrityError:
                return render(request, 'signup.html', {'error_message': "Username already exists. Please choose a different username."})

    return render(request, 'signup.html')

@csrf_protect
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        # Authenticating user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html',{'error_message': "Username or password is wrong. Please try again."})

    return render(request, 'login.html')

@login_required
def LogoutPage(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

def ForgotPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        rpass1 = request.POST.get('rpassword1')
        rpass2 = request.POST.get('rpassword2')

        if rpass1 != rpass2:
            return render(request, 'forgotpassword.html', {'error_message': "Passwords do not match. Please try again."})
        else:
            try:
                my_user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, 'forgotpassword.html', {'error_message': "User does not exist."})

            my_user.set_password(rpass1)
            my_user.save()
            return render(request, 'password_change_success.html', {'message': "Password changed successfully. You can now log in."})

    return render(request, 'forgotpassword.html')