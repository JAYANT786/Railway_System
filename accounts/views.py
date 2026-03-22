from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random

# TEMP OTP STORAGE
otp_storage = {}


# ------------------ REGISTER ------------------
def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'User already exists'
            })

        # Generate OTP
        otp = str(random.randint(1000, 9999))
        otp_storage[username] = otp

        # Save data in session
        request.session['username'] = username
        request.session['password'] = password

        return render(request, 'otp.html', {
            'otp': otp   # 👈 SHOW OTP ON SCREEN
        })

    return render(request, 'register.html')


# ------------------ VERIFY OTP ------------------
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')

        username = request.session.get('username')
        password = request.session.get('password')

        if otp_storage.get(username) == entered_otp:
            # Create user
            User.objects.create_user(username=username, password=password)

            # Clear session
            request.session.flush()

            return redirect('/login/?registered=true')
        else:
            return render(request, 'otp.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'otp.html')


# ------------------ LOGIN ------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/?login_success=true')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')


# ------------------ LOGOUT ------------------
def logout_user(request):
    logout(request)
    return redirect('/login/')


# ------------------ FORGOT PASSWORD ------------------
def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('/forgot/')

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully! Please login with new password.")
            return redirect('/login/')
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('/forgot/')

    return render(request, 'forgot.html')